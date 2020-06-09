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
            active_cases = total_no_confirmed - total_no_deaths - total_no_cured
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
            htmlfilestr = '<html>\n'+'<body style="background-color:white;">\n'+ \
            '<h1>'+ 'Corona Virus Situation of '+self.name+ '</h1>\n'+ \
            '<p>'+ 'Duration 30th jan 2020 to 7th june 2020'+'</p>\n'+ \
            '<p>'+'Total number of confirmed case: '+str(total_no_confirmed)+'</p>\n'+ \
            '<p>'+ 'Active Cases: '+ str(active_cases)+ '</p>\n'+ \
            '<p>' + 'Total number of Deaths: ' + str(total_no_deaths) + '</p>\n'+ \
            '<p>' + 'Total number of people Recovered: ' + str(total_no_cured) + '</p>\n'+ \
            html_image + \
            html_image1 + \
            '<h2>'+ 'Safety Measures provided by WHO(World Health Organinzation) to fight against Corona virus' + '</h2>\n'+ \
            '<p>'+ 'Regularly and thoroughly clean your hands with an alcohol-based hand rub or wash them with soap and water. ' \
                   'Why? Washing your hands with soap and water or using alcohol-based hand rub kills viruses that may be on your hands.' + '</p>\n'+ \
            '<p>'+ 'Maintain at least 1 metre (3 feet) distance between yourself and others. Why? When someone coughs, sneezes, ' \
                   'or speaks they spray small liquid droplets from their nose or mouth which may contain virus. ' \
                   'If you are too close, you can breathe in the droplets, including the COVID-19 virus if the person has the disease.'+ '</p>\n'+ \
            '<p>' + 'Avoid going to crowded places. Why? Where people come together in crowds, you are more likely to come into close contact ' \
                    'with someone that has COIVD-19 and it is more difficult to maintain physical distance of 1 metre (3 feet)' + '</p>\n' + \
            '<p>' + 'Stay home and self-isolate even with minor symptoms such as cough, headache, mild fever, until you recover. Have someone bring you supplies.' \
                    ' If you need to leave your house, wear a mask to avoid infecting others. Why? Avoiding contact with others will protect them from possible COVID-19 ' \
                    'and other viruses.'+ '</p>\n'+ \
            '<p>' + 'If you have a fever, cough and difficulty breathing, seek medical attention, but call by telephone in advance if possible and follow the directions of your' \
                    ' local health authority. Why? National and local authorities will have the most up to date information on the situation in your area. ' \
                    'Calling in advance will allow your health care provider to quickly direct you to the right health facility. This will also protect you and help prevent' \
                    ' spread of viruses and other infections.' + '</p>\n'+ \
            '<p>' + 'Keep up to date on the latest information from trusted sources, such as WHO or your local and national health authorities. Why? Local and national ' \
                    'authorities are best placed to advise on what people in your area should be doing to protect themselves.'+ '</p>\n' + \
            '</body>\n'+'</html>'
            return htmlfilestr
        except Exception as e:
            print('Error: ', e)

