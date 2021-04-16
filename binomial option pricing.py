import numpy as np

class Bioptionprice:
    def __init__(self, s0, u, r, k, N):
        self.init_price = s0
        self.up_change = u
        self.riskfree_rate = r
        self.strike_price = k
        # from model
        self.down_change = 1 / self.up_change
        self.up_prob = (1 + self.riskfree_rate - self.down_change) / (self.up_change - self.down_change)
        self.down_prob = 1 - self.up_prob

        self.N = N
        self.stock = np.zeros([self.N + 1, self.N + 1])
        self.option = np.zeros([self.N + 1, self.N + 1])

    def stock_price_path(self):
        for i in range(self.N + 1):
            for j in range(self.N + 1): # for each columns, there are N time to choose
                self.stock[j, i] = self.init_price * (self.up_change ** (i - j)) * (self.down_change ** j)

        return self.stock

    def option_price_path(self):
        self.option[:, self.N] = np.maximum(np.zeros(self.N + 1), (self.stock[:, self.N] - self.strike_price))
        for i in range(self.N - 1, -1, -1):
            for j in range(0, i + 1):
                self.option[j, i] = (1 / (1 + self.riskfree_rate) * (self.up_prob * self.option[j, i+1]
                                     + self.down_prob * self.option[j+1, i+1]))

        return self.option

    def see_results(self):
        stock_table = self.stock_price_path()
        print('==== stock path ====')
        print(stock_table)
        option_table = self.option_price_path()
        print('==== option path ====')
        print(option_table)



if __name__ == '__main__':
    # s0, u, r, k, N
    agent = Bioptionprice(s0 = 4, u=2, r=0.25, k=8, N = 5)
    agent.see_results()
