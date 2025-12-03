import pandas as pd
import numpy as np 
import scipy.stats as stats
from .backend import market_prices

def portfolio_volatility(
       df:pd.DataFrame,
       vector_w:np.array
       ) -> float:
   '''
   Calculo de la volatilidad de un portafolio de inversiones. 
   entendemos la volatilidad como la dispercion de los retornos
   futuros de un actv.fin

   df(pd.DataFrame):
   dataframe de retornos de portsfolio 
   vector_w (np.array)
   vector de pesos de los instrumentos de portafolio 
   return (float): volatilidad de portafolio 
   '''

   # matriz varianza covarianza 
   m_cov = df.cov()

   #vector transpuesto 
   vector_w_t = np.array([vector_w])

   #varianza
   vector_cov = np.dot(m_cov,vector_w)
   varianza = np.dot(vector_w_t,vector_cov)

   #volatilidad 
   vol = np.sqrt(varianza)

   return vol[0]

def portfolio_returns(
         tickers: list,
         start: str, 
         end: str,
         ) -> pd.DataFrame:

   '''
   Descarga desde a base de datos los precios de los instrumentos
   indicados en el rango de fechas.

   tickers (list): lista de instrumentos financieros que componen el portafolio 
   start (str): fecha de inicio de precios  en formato 'YYYY-MM-DD'
   end (str): fecha de terminode precios en formato 'YYYY-MM-DD'
   return (pd.DataFrame): dataframe de retornos de portafolio diarios  
   '''

   #descargar precios
   df = market_prices(
   start_date = start,
   end_date = end,
   tickers = tickers
   )

   # pivot retornos 
   df_pivot = pd.pivot_table(
   data=df,
   index='FECHA',
   columns='TICKER',
   values='PRECIO_CIERRE',
   aggfunc='max'
   )

   df_pivot = df_pivot.pct_change().dropna()

   return df_pivot

def VaR(sigma:float, confidence:float) -> float:
   '''
   Calculo del Valor en Riesgo (VaR) de un portafolio de inversiones
   segun el nivel de confianza indicado.

   sigma (float): volatilidad del portafolio 
   confidence (float): nivel de confianza para el calculo de VaR 
   return (float): Valor en Riesgo del portafolio 
   '''

   #esradistico z segun nivel de confianza
   z_score = stats.norm.ppf(confidence)

    #VaR
   var = z_score * sigma

   return var

   #calcualr el var de todos los etf yinjab ejecutar el archivo main me tienen que mandar un risk ranquiado de mayor menor (ordenarlo por riesgo de mercado) 

   