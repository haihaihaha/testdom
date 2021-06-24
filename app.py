
from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px

import csv, re, operator
# from textblob import TextBlob

app = Flask(__name__)

person = {
	'first_name': 'Y',
	'last_name' : 'X',
	'address' : 'Normal University',
	'job': 'Web developer',
	'tel': '0678282923',
	'email': '1234567890@yahoo.com',
	'qq':'11111111',
	'wechat':'11111111',
	'description' : '本人性格开朗与人处事融洽，对工作善始善终，能承受日益严重的竞争压力，并能在成功与失败中完善自己。\n活泼开朗乐观向上适应力强勤奋好学认真负责坚毅不拔勇于迎接新挑战。擅长业务具有良好的沟通潜力与团队合作精神。',
	'social_media' : [
		{
			'link': 'https://www.csdn.net/',
			'icon' : ''
		},
		{
			'link': 'https://github.com/',
			'icon' : 'fa-github'
		},
		{
			'link': 'https://www.cnblogs.com/',
			'icon' : ''
		},
		{
			'link': 'https://twitter.com/',
			'icon' : 'fa-weixin'
		}
	],
	'img': 'img/img_nono.jpg',
	'experiences' : [
		{
			'title' : 'Web Developer',
			'company': 'AZULIK',
			'description' : 'Project manager and lead developer for several AZULIK websites.',
			'timeframe' : 'July 2018 - November 2019'
		},
		{
			'title' : 'Freelance Web Developer',
			'company': 'Independant',
			'description' : 'Create Wordpress websites for small and medium companies. ',
			'timeframe' : 'February 2017 - Present'
		},
		{
			'title' : 'Sharepoint Intern',
			'company': 'ALTEN',
			'description' : 'Help to manage a 600 Sharepoint sites platform (audit, migration to Sharepoint newer versions)',
			'timeframe' : 'October 2015 - October 2016'
		}
	],
	'education' : [
		{
			'university': 'Paris Diderot',
			'degree': 'Projets informatiques et Startégies d\'entreprise (PISE)',
			'description' : 'Gestion de projets IT, Audit, Programmation',
			'mention' : 'Bien',
			'timeframe' : '2015 - 2016'
		},
		{
			'university': 'Paris Dauphine',
			'degree': 'Master en Management global',
			'description' : 'Fonctions supports (Marketing, Finance, Ressources Humaines, Comptabilité)',
			'mention' : 'Bien',
			'timeframe' : '2015'
		},
		{
			'university': 'Lycée Turgot - Paris Sorbonne',
			'degree': 'CPGE Economie & Gestion',
			'description' : 'Préparation au concours de l\'ENS Cachan, section Economie',
			'mention' : 'N/A',
			'timeframe' : '2010 - 2012'
		}
	],
	'programming_languages' : {
		'HMTL' : ['fa-html5', '100'], 
		'CSS' : ['fa-css3-alt', '100'], 
		'SASS' : ['fa-sass', '90'], 
		'JS' : ['fa-js-square', '90'],
		'Wordpress' : ['fa-wordpress', '80'],
		'Python': ['fa-python', '70'],
		'Mongo DB' : ['fa-database', '60'],
		'MySQL' : ['fa-database', '60'],
		'NodeJS' : ['fa-node-js', '50']
	},
	'languages' : {'英语' : '六级'},
	'interests' : ['羽毛球', '旅游', '语言', '电影']
}

@app.route('/')
def cv(person=person):
	return render_template('index.html', person=person)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
	return gm(request.args.get('data'))
   
@app.route('/chart')
def index():
	res=gm()
	return render_template('chartsajax.html',  graphJSON=res[0],graphJSON1=res[1],graphJSON2=res[2],graphJSON3=res[3],graphJSON4=res[4],graphJSON5=res[5],graphJSON6=res[6])

@app.route('/chart1')
def index1():
	res=tips()
	return render_template('chartsajax1.html',  graphJSON=res[0],graphJSON1=res[1],graphJSON2=res[2],graphJSON3=res[3],graphJSON4=res[4],graphJSON5=res[5],graphJSON6=res[6],graphJSON7=res[7])

@app.route('/chart2')
def index2():
	res=election()
	return render_template('chartsajax2.html',  graphJSON=res[0],graphJSON1=res[1])

@app.route('/chart3')
def index3():
	res=wind()
	return render_template('chartsajax3.html',  graphJSON=res[0],graphJSON1=res[1],graphJSON2=res[2])

def gm(country='United Kingdom'):
	df = pd.DataFrame(px.data.gapminder())

	fig = px.scatter(df[df['country']==country], x="year", y="lifeExp")

	fig1 = px.bar(df[df['country']==country], x="year", y="gdpPercap")

	fig2=px.scatter(df[df['year']==2007], x="gdpPercap", y="lifeExp",color='continent')

	fig3=px.scatter(df[df['year']==2007], x="gdpPercap", y="lifeExp",color='continent',size='pop',size_max=60,hover_name='country')

	fig4=px.scatter(df[df['year']==2007], x="gdpPercap", y="lifeExp",color='continent',size='pop',size_max=60,hover_name='country',facet_col='continent',log_x=True)

	fig5=px.scatter(df, x='gdpPercap', y='lifeExp',
           color='continent', size='pop', size_max=60,
           animation_frame='year', animation_group='country',
          range_y = [30,100], range_x = [-5000,55000],
          labels = {'gdpPercap':'GDP', 'lifeExp':'Life Expectancy'})

	fig6=px.choropleth(df,locations='iso_alpha',color='lifeExp',hover_name='country',animation_frame='year',color_continuous_scale=px.colors.sequential.Plasma,projection='natural earth')

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON,graphJSON1,graphJSON2,graphJSON3,graphJSON4,graphJSON5,graphJSON6

	

def election():
	election = pd.DataFrame(px.data.election())

	fig = px.scatter_3d(election,x="Joly",y="Coderre",z="Bergeron"  # 指定3个轴
		,color="winner",size="total",hover_name="district_id"  # 指定颜色种类、大小和显示名称
    	,symbol="result"  # 右边的圆形和菱形
    	,color_discrete_map={"Joly":"blue","Bergeron":"green","Coderre":"red"}   # 改变默认颜色
        )

	fig1=px.line_3d(election,x="Joly",y="Coderre",z="Bergeron",color="winner",line_dash="winner")

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON,graphJSON1

def wind():
	#wind
	wind = pd.DataFrame(px.data.wind())
	fig = px.scatter_polar(wind,r="frequency",theta="direction",color="strength",symbol="strength",color_discrete_sequence=px.colors.sequential.Plasma_r)

	fig1 = px.line_polar(wind,r="frequency",theta="direction",color="strength",line_close=True,color_discrete_sequence=px.colors.sequential.Plasma_r)

	fig2 = px.bar_polar(wind,r="frequency",theta="direction",color="strength",template="plotly_dark",color_discrete_sequence=px.colors.sequential.Plasma_r)

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON,graphJSON1,graphJSON2

def tips():
	#tips
	df = pd.DataFrame(px.data.tips())

	fig = px.histogram(df, x="total_bill", y="tip",histfunc="sum",color="smoker")
	fig1=px.histogram(df,x="sex",y="tip",histfunc="avg",color="smoker",barmode="group",facet_row="time",facet_col="day",category_orders={"day":["Thur","Fri","Sat","Sun"],"time":["Lunch","Dinner"]})

	fig2=px.box(df,x='total_bill',y='day',orientation='h',color='smoker',notched=True,category_orders={'day':['Thur','Fri','Sat','Sun']})

	fig3=px.violin(df,y='tip',x='smoker',color='sex',box=True,points='all',hover_data=df.columns)

	fig4=px.scatter(df,x='total_bill',y='tip',color='smoker',trendline='ols',marginal_x='violin',marginal_y='box')

	fig5 = px.scatter(df,x="total_bill",y="tip",color="size",render_mode="webgl",facet_col="sex",color_continuous_scale=px.colors.sequential.Viridis)

	fig6 = px.parallel_categories(df,color="size",color_continuous_scale=px.colors.sequential.Inferno)

	fig7 = px.bar(df,x="sex",y="total_bill",color="smoker",barmode="group",facet_row="time",facet_col="day",category_orders={"day": ["Thur","Fri","Sat","Sun"],"time":["Lunch", "Dinner"]})

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON6 = json.dumps(fig6, cls=plotly.utils.PlotlyJSONEncoder)
	graphJSON7 = json.dumps(fig7, cls=plotly.utils.PlotlyJSONEncoder)


	return graphJSON,graphJSON1,graphJSON2,graphJSON3,graphJSON4,graphJSON5,graphJSON6,graphJSON7


@app.route('/senti')
def main():
	text = ""
	values = {"positive": 0, "negative": 0, "neutral": 0}

	with open('ask_politics.csv', 'rt') as csvfile:
		reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
		for idx, row in enumerate(reader):
			if idx > 0 and idx % 2000 == 0:
				break
			if  'text' in row:
				nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
				text = nolinkstext

			blob = TextBlob(text)
			for sentence in blob.sentences:
				sentiment_value = sentence.sentiment.polarity
				if sentiment_value >= -0.1 and sentiment_value <= 0.1:
					values['neutral'] += 1
				elif sentiment_value < 0:
					values['negative'] += 1
				elif sentiment_value > 0:
					values['positive'] += 1

	values = sorted(values.items(), key=operator.itemgetter(1))
	top_ten = list(reversed(values))
	if len(top_ten) >= 11:
		top_ten = top_ten[1:11]
	else :
		top_ten = top_ten[0:len(top_ten)]

	top_ten_list_vals = []
	top_ten_list_labels = []
	for language in top_ten:
		top_ten_list_vals.append(language[1])
		top_ten_list_labels.append(language[0])

	graph_values = [{
					'labels': top_ten_list_labels,
					'values': top_ten_list_vals,
					'type': 'pie',
					'insidetextfont': {'color': '#FFFFFF',
										'size': '14',
										},
					'textfont': {'color': '#FFFFFF',
										'size': '14',
								},
					}]

	layout = {'title': '<b>意见挖掘</b>'}

	return render_template('sentiment.html', graph_values=graph_values, layout=layout)


if __name__ == '__main__':
  app.run(debug= True,port=5000,threaded=True)
