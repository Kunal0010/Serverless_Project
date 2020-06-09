import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import pathlib


class CoronaUpdate:
    def __init__(self, name):
        self.name = name
        file_name = pathlib.Path(__file__).parent / 'covid_19_india.csv'
        self.df = pd.read_csv(file_name)

    def reverse_cumulative(self,cumulative):
        output = [0] * len(cumulative)
        for i in range(len(cumulative) - 1):
            output[i + 1] = cumulative[i + 1] - cumulative[i]
        output[0] = cumulative[0]
        return output

    def sub_data(self):
        try:
            sub_df = self.df.copy()
            state = self.name
            sub_df = sub_df.loc[(self.df['State/UnionTerritory'] == state)]
            sub_df.drop(['ConfirmedIndianNational', 'ConfirmedForeignNational'], axis=1, inplace=True)
            sub_df = sub_df.reset_index()
            cured_per_day = self.reverse_cumulative(sub_df['Cured'])
            confirmed_per_day = self.reverse_cumulative(sub_df['Confirmed'])
            deaths_per_day = self.reverse_cumulative(sub_df['Deaths'])
            sub_df['Cured per day'] = cured_per_day
            sub_df['Confirmed per day'] = confirmed_per_day
            sub_df['Deaths per day'] = deaths_per_day
            total_no_confirmed = sub_df['Confirmed'].iloc[-1]
            total_no_deaths =  sub_df['Deaths'].iloc[-1]
            total_no_cured = sub_df['Cured'].iloc[-1]
            #first graph
            fig = plt.figure()
            plt.plot('Date', 'Confirmed', data=sub_df, marker='', color='skyblue', linewidth=2)
            plt.plot('Date', 'Cured', data=sub_df, marker='', color='olive', linewidth=2)
            plt.plot('Date', 'Deaths', data=sub_df, marker='', color='red', linewidth=2)
            plt.legend()
            tmpfile = BytesIO()
            fig.savefig(tmpfile, format='png')
            encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
            html_image ='<img src=\"data:image/png;base64,{}\" style=\"height:836px; width:592px\">\n'.format(encoded)
            #second graph
            fig1 = plt.figure()
            plt.plot('Date', 'Cured per day', data=sub_df, marker='', color='skyblue', linewidth=2)
            plt.plot('Date', 'Confirmed per day', data=sub_df, marker='', color='olive', linewidth=2)
            plt.plot('Date', 'Deaths per day', data=sub_df, marker='', color='red', linewidth=2)
            plt.legend()
            tmpfile1 = BytesIO()
            fig1.savefig(tmpfile1, format='png')
            encoded1 = base64.b64encode(tmpfile1.getvalue()).decode('utf-8')
            html_image1 = '<img src=\"data:image/png;base64,{}\" style=\"height:836px; width:592px\">\n'.format(
                encoded1)
            '''
            file_name = pathlib.Path(__file__).parent / 'State13.html'
            with open(file_name, 'w') as f:
                f.write('<html>\n'+'<body style="background-color:pink;">\n')
                f.write('<h1>'+ 'Corona Virus Situation of '+self.name+ '</h1>\n')
                f.write('<p>'+ 'Duration 30th jan 2020 to 7th june 2020'+'</p>\n')
                f.write('<p>'+'Total number of confirmed case: '+str(total_no_confirmed)+'</p>\n')
                f.write('<p>' + 'Total number of Deaths: ' + str(total_no_deaths) + '</p>\n')
                f.write('<p>' + 'Total number of people Recovered: ' + str(total_no_cured) + '</p>\n')
                f.write(html_image)
                f.write(html_image1)
                f.write('</body>\n'+'</html>' )
                f.close()
            '''
            htmlfilestr = '<html>\n'+'<body style="background-color:pink;">\n'+ \
            '<h1>'+ 'Corona Virus Situation of '+self.name+ '</h1>\n'+ \
            '<p>'+ 'Duration 30th jan 2020 to 7th june 2020'+'</p>\n'+ \
            '<p>'+'Total number of confirmed case: '+str(total_no_confirmed)+'</p>\n'+ \
            '<p>' + 'Total number of Deaths: ' + str(total_no_deaths) + '</p>\n'+ \
            '<p>' + 'Total number of people Recovered: ' + str(total_no_cured) + '</p>\n'+ \
            html_image + \
            html_image1 + \
            '</body>\n'+'</html>'
            return htmlfilestr
        except Exception as e:
            print('Error: ', e)

