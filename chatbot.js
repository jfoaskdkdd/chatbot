const wppconnect = require('@wppconnect-team/wppconnect');
const contatos = require('./contatos_filtrados.json');
const fs = require('fs');

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function randomDelay(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function normalizarNomeContato(contato) {
  // Se o contato veio do Google, pode ter campos separados
  if (contato.firstName || contato.middleName || contato.lastName) {
    return [contato.firstName || '', contato.middleName || '', contato.lastName || '']
      .join(' ').replace(/ +/g, ' ').trim();
  }
  // Se veio do JSON, já está em contato.nome
  return contato.nome ? contato.nome.replace(/ +/g, ' ').trim() : '';
}

function removerAcentos(str) {
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}

let enviados = 0;
let falhas = 0;

console.log('🚀 Bot iniciado. Lendo lista de contatos...');
console.log(`Total de contatos para envio: ${contatos.length}`);

wppconnect.create({
  session: 'disparador',
  catchQR: (base64Qr, asciiQR, attempts, urlCode) => {
    console.log('🔗 Escaneie o QR Code para parear o WhatsApp!');
    // Opcional: mostrar o QR em ASCII no terminal
    console.log(asciiQR);
  },
  statusFind: (statusSession, session) => {
    console.log(`📡 Status da sessão: ${statusSession}`);
  }
}).then(async (client) => {
  console.log('✅ Conectado à sessão do WhatsApp!');
  const todosContatos = await client.getAllContacts();
  for (let i = 0; i < contatos.length; i++) {
    const contato = contatos[i];
    const nomeBusca = removerAcentos(normalizarNomeContato(contato).toLowerCase().replace(/ +/g, ' '));
    const mensagem = `Opa! Tudo certo? Fiz um site pra vc, posso te apresentar?`;
    try {
      // Log detalhado de todos os contatos (apenas uma vez)
      if (i === 0) {
        fs.writeFileSync('log_contatos_wpp.txt', 'id | name | isMyContact | normalizado\n');
        todosContatos.forEach(c => {
          if (c.name) {
            fs.appendFileSync('log_contatos_wpp.txt', `${c.id} | ${c.name} | ${c.isMyContact} | ${removerAcentos(c.name.toLowerCase().replace(/ +/g, ' '))}\n`);
          }
        });
      }
      // Busca exata
      let contatoAgenda = todosContatos.find(c =>
        c.name &&
        removerAcentos(c.name.toLowerCase().replace(/ +/g, ' ')) === nomeBusca
      );
      // Se não achou, busca por substring
      if (!contatoAgenda) {
        contatoAgenda = todosContatos.find(c =>
          c.name &&
          removerAcentos(c.name.toLowerCase().replace(/ +/g, ' ')).includes(nomeBusca)
        );
      }
      if (contatoAgenda && contatoAgenda.id && contatoAgenda.isMyContact) {
        console.log(`➡️ [${i+1}/${contatos.length}] Enviando mensagem para ${normalizarNomeContato(contato)} (${contatoAgenda.id})...`);
        try {
          await client.sendText(contatoAgenda.id, mensagem);
          console.log(`✅ Mensagem enviada para ${normalizarNomeContato(contato)} (${contatoAgenda.id})`);
          enviados++;
        } catch (erroEnvio) {
          console.log(`❌ Falha ao enviar mensagem para ${normalizarNomeContato(contato)} (${contatoAgenda.id}): ${erroEnvio.message}`);
          // Tenta enviar uma segunda mensagem imediatamente
          try {
            await client.sendText(contatoAgenda.id, mensagem);
            console.log(`✅ Mensagem enviada na segunda tentativa para ${normalizarNomeContato(contato)} (${contatoAgenda.id})`);
            enviados++;
          } catch (erroEnvio2) {
            console.log(`❌ Segunda tentativa falhou para ${normalizarNomeContato(contato)} (${contatoAgenda.id}): ${erroEnvio2.message}`);
            falhas++;
          }
        }
      } else {
        // Log detalhado de pesquisa na agenda
        const nomesComparados = todosContatos
          .filter(c => c.name)
          .map(c => {
            return {
              original: c.name,
              normalizado: removerAcentos(c.name.toLowerCase().replace(/ +/g, ' '))
            };
          });
        fs.appendFileSync('log_pesquisa.txt', `Contato não encontrado: ${normalizarNomeContato(contato)} | Busca: ${nomeBusca}\n`);
        fs.appendFileSync('log_pesquisa.txt', `Nomes comparados:\n`);
        nomesComparados.forEach(nc => {
          fs.appendFileSync('log_pesquisa.txt', `- original: ${nc.original} | normalizado: ${nc.normalizado}\n`);
        });
        fs.appendFileSync('log_pesquisa.txt', `-----------------------------\n`);
        console.log(`⚠️ [${i+1}/${contatos.length}] Contato não encontrado na agenda: ${normalizarNomeContato(contato)} - pulando.`);
        falhas++;
      }
    } catch (e) {
      console.log(`❌ [${i+1}/${contatos.length}] Erro ao processar ${normalizarNomeContato(contato)}: ${e.message}`);
      falhas++;
    }
    const restantes = contatos.length - (i+1);
    console.log(`📊 Progresso: ${enviados} enviados, ${falhas} falhas, ${restantes} restantes.`);
    const espera = randomDelay(60000, 80000); // 1 a 1 minuto e 20 segundos
    console.log(`⏳ Aguardando ${Math.round(espera/1000)} segundos antes do próximo envio...`);
    await delay(espera);
  }
  fs.writeFileSync('log.txt', `Enviados: ${enviados}\nFalhas: ${falhas}`);
  console.log(`📊 Envio finalizado: ${enviados} enviados, ${falhas} falhas`);
}).catch((err) => {
  console.log('❌ Erro ao iniciar o bot:', err.message);
});
