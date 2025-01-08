import ccxt
import time

# Configuração inicial
GREEN_LINE = 1.2400  # Preço barato
WHITE_LINE = 1.2500  # Preço justo
RED_LINE = 1.2600    # Preço caro
LOT_SIZE = 0.01      # Tamanho do lote
SYMBOL = "BTC/USDT"  # Símbolo a ser operado (par de criptomoedas)

# Configuração da API da exchange (exemplo: Binance)
exchange = ccxt.binance({
    "apiKey": "SUA_API_KEY",
    "secret": "SEU_API_SECRET",
})

# Função para verificar o preço atual
def get_current_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return ticker['bid'], ticker['ask']

# Função para abrir ordens
def open_trade(action, symbol, lot):
    if action == "buy":
        order = exchange.create_market_buy_order(symbol, lot)
    elif action == "sell":
        order = exchange.create_market_sell_order(symbol, lot)
    print(f"Ordem {action} enviada:", order)

# Lógica principal
def main():
    print("Robô iniciado. Monitorando os preços...")
    while True:
        bid, ask = get_current_price(SYMBOL)

        # Simular posições abertas
        # Para simplificação, assumimos que só existe uma posição por vez
        current_position = None

        # Comprar quando o preço atingir a linha verde
        if bid <= GREEN_LINE and current_position is None:
            print(f"Preço barato detectado ({bid}). Comprando...")
            open_trade("buy", SYMBOL, LOT_SIZE)
            current_position = "buy"

        # Vender quando o preço atingir a linha vermelha
        if ask >= RED_LINE and current_position is None:
            print(f"Preço caro detectado ({ask}). Vendendo...")
            open_trade("sell", SYMBOL, LOT_SIZE)
            current_position = "sell"

        # Fechar compras quando o preço atingir a linha branca
        if bid >= WHITE_LINE and current_position == "buy":
            print(f"Preço justo detectado ({bid}). Fechando posição de compra...")
            open_trade("sell", SYMBOL, LOT_SIZE)
            current_position = None

        # Fechar vendas quando o preço atingir a linha branca
        if ask <= WHITE_LINE and current_position == "sell":
            print(f"Preço justo detectado ({ask}). Fechando posição de venda...")
            open_trade("buy", SYMBOL, LOT_SIZE)
            current_position = None

        time.sleep(1)  # Intervalo de 1 segundo entre verificações

# Executar o robô
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Robô encerrado pelo usuário.")
