#import MetaTrader5 as mt5  versao correta
import ccxt as mt5
import time

# Configuração inicial
GREEN_LINE = 1.2400  # Preço barato
WHITE_LINE = 1.2500  # Preço justo
RED_LINE = 1.2600    # Preço caro
LOT_SIZE = 0.01      # Tamanho do lote
SYMBOL = "GBPUSD"    # Símbolo a ser operado

# Inicializa conexão com o MetaTrader 5
if not mt5.initialize():
    print("Erro ao inicializar o MetaTrader 5:", mt5.last_error())
    quit()

# Função para verificar o preço atual
def get_current_price(symbol):
    tick = mt5.symbol_info_tick(symbol)
    if tick is not None:
        return tick.bid, tick.ask  # Retorna bid e ask
    else:
        print("Erro ao obter o preço do ativo:", mt5.last_error())
        return None, None

# Função para abrir ordens
def open_trade(action, symbol, lot, price, deviation=20):
    order_type = mt5.ORDER_BUY if action == "buy" else mt5.ORDER_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": deviation,
        "magic": 123456,  # Número mágico para identificar as ordens
        "comment": "Trade Automático",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Erro ao enviar a ordem {action}:", result)
    else:
        print(f"Ordem {action} executada com sucesso:", result)

# Função para fechar ordens
def close_trade(order, lot, price, deviation=20):
    order_type = mt5.ORDER_SELL if order.type == mt5.ORDER_BUY else mt5.ORDER_BUY
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": order.symbol,
        "volume": lot,
        "type": order_type,
        "position": order.ticket,
        "price": price,
        "deviation": deviation,
        "magic": order.magic,
        "comment": "Fechando ordem",
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Erro ao fechar a ordem:", result)
    else:
        print("Ordem fechada com sucesso:", result)

# Função para buscar ordens abertas
def get_open_positions(symbol):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("Erro ao obter posições abertas:", mt5.last_error())
        return []
    return positions

# Lógica principal
def main():
    print("Robô iniciado. Monitorando os preços...")
    while True:
        bid, ask = get_current_price(SYMBOL)
        if bid is None or ask is None:
            time.sleep(1)
            continue

        # Verificar posições abertas
        positions = get_open_positions(SYMBOL)
        buy_position = any(p.type == mt5.ORDER_BUY for p in positions)
        sell_position = any(p.type == mt5.ORDER_SELL for p in positions)

        # Comprar quando o preço atingir a linha verde
        if bid <= GREEN_LINE and not buy_position:
            open_trade("buy", SYMBOL, LOT_SIZE, ask)

        # Vender quando o preço atingir a linha vermelha
        if ask >= RED_LINE and not sell_position:
            open_trade("sell", SYMBOL, LOT_SIZE, bid)

        # Fechar compras quando o preço atingir a linha branca
        if bid >= WHITE_LINE and buy_position:
            for position in positions:
                if position.type == mt5.ORDER_BUY:
                    close_trade(position, position.volume, bid)

        # Fechar vendas quando o preço atingir a linha branca
        if ask <= WHITE_LINE and sell_position:
            for position in positions:
                if position.type == mt5.ORDER_SELL:
                    close_trade(position, position.volume, ask)

        time.sleep(1)  # Intervalo de 1 segundo entre verificações

# Encerrar conexão ao terminar
def shutdown():
    mt5.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Robô encerrado pelo usuário.")
    finally:
        shutdown()
