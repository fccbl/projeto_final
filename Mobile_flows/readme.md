## Mobile Flows – Jornada de Compra no App Americanas
## 🎯 Objetivo

### Validar o fluxo completo de compra de produtos no aplicativo da Americanas, utilizando os 3 produtos retornados pela wishlist da API do projeto_final.
O teste garante que as informações exibidas (nome, preço e frete) estejam corretas e que o processo de compra funcione até a tela de checkout.

🧾 Resumo do Cenário

- Abrir o aplicativo da Americanas.
- Buscar um produto retornado pela wishlist da API.
- Selecionar o produto correto nos resultados.
- Validar a página do produto:
- Nome e preço correspondem ao retorno da API.
- Inserir um CEP inválido e validar mensagem de erro.
- Inserir o CEP válido da API e validar o cálculo de frete e prazo de entrega.
- Adicionar o produto ao carrinho.
- Validar o popup do carrinho:
- Nome e preço corretos.
- Aumentar quantidade para 2 unidades e validar atualização.
- Diminuir para 1 unidade e verificar que o botão “–” fica inativo.
- Aumentar novamente para 2 unidades.
- Acessar a tela de finalização.
- Validar o carrinho final:
- Nome e quantidade corretos.
- Subtotal e total dobrando o valor unitário.
- Valor do botão “Finalizar compra” refletindo o total de duas unidades.
- Repetir teste de CEP inválido e válido.
- Prosseguir para o checkout.
- Validar o redirecionamento para a tela de login com a mensagem:
“Informe seu e-mail para continuar”.