# Desafio Back-end

<h2>Problema:</h2>
<p>Criar uma API de controle de estacionamento:</p>
<ul> ● Deve registrar entrada, saída e pagamento por placa;</ul>
<ul> ● Não deve liberar saída sem pagamento;</ul>
<ul> ● Deve fornecer um histórico por placa.</ul>
<p> Essa api deve respeitar os status http corretamente, deve aceitar e responder por json.  </p>

<h2> Ações que devem estar disponíveis: </h2>
<h3> Entrada: </h3>
  <p>  POST /parking </p>
  <p>  { plate: 'FAA-1234' } </p>
  <p>  Deve retornar um número de "reserva" e validar a máscara AAA-9999  </p>

<h3>  Saída: </h3>
   <p>   PUT /parking/:id/out </p>

<h3> Pagamento: </h3>
<p>  PUT /parking/:id/pay </p>

<h3> Histórico: </h3>
   <p> GET /parking/:plate </p>
<p> {id: 42, time: '25 minutes', paid: true, left: false} </p>

<h2>Tecnologia usada </h2>
<p>A tecnologia utilizada foi python 3.11 com JSON. As bibliotecas utilizadas foram: </p>
<ul> ● Flask, responsável por fazer os caminhos das API</ul>
<ul> ● Request, responsável por trafegar os dados </ul>
<ul> ● Jsonfy, responsável por transmitir as mensagens em JSON</ul>
<ul> ● Datatime, responsável por calcular as horas no estacionamento</ul>
<ul> ● os, responsável pela criação do arquivo JSON</ul>

