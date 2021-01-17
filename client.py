import requests
import json
import matplotlib.pyplot as plt


class Client(object):
    def __init__(self):

        self.url = "https://trontrade.io/graphql/"

    def dex_stats(self):
        """

        :return:
        """

        stats = """query {
            stats {
            traders24hActive 
            volume24hTrx
            }
        }"""
        re = requests.post(self.url, json={'query': stats})
        if re.status_code == 200:

            return json.loads(re.text)["data"]["stats"]

    def get_pairs(self):
        """

        :return:
        """
        exchange_pairs = """

            query {


          exchanges {
            id
            buyAssetName
            sellAssetName
            stats {
              lastPrice
              h24_price
              h24_change
              volume
            }
          }


            }

        """
        re = requests.post(self.url, json={'query': exchange_pairs})
        if re.status_code == 200:
            return json.loads(re.text)["data"]["exchanges"]

    def plot_top_volume(self):
        """

        :return:
        """
        data_list = list(Client().get_pairs())

        positive_vol, pairs_name, volume = [], [], []

        for pair in data_list:
            if pair["stats"]["volume"] == 0:
                continue
            else:
                positive_vol.append(pair)

        for pair in positive_vol:
            pairs_name.append(pair["buyAssetName"])

        coingecko = requests.get("https://api.coingecko.com/api/v3/coins/tron")
        trx_price = json.loads(coingecko.text)["market_data"]["current_price"]["usd"]

        for pair in positive_vol:
            print(pair["stats"]["lastPrice"])
            print(pair["stats"]["volume"])
            print(pair)
            if pair["buyAssetName"] == 'SUN' or 'JST':
                volume.append( int(pair["stats"]["lastPrice"]) / 1000000 * int(pair["stats"]["volume"]) * 1e-18)
            else:
                volume.append(int(pair["stats"]["lastPrice"]) / 1000000 * int(pair["stats"]["volume"]) * 1e-6)

        print(f"volume {volume}")

        plt.bar(pairs_name, volume)
        plt.show()



print(Client().plot_top_volume())
