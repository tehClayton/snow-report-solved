from flask import Flask, render_template, redirect
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.sql.expression import func
import scraper
from ski_resort import SkiResort, Base
from config import mysql_un, mysql_pw, mysql_uri, mysql_port
from datetime import datetime

app = Flask(__name__)

connection_string = f"mysql://{mysql_un}:{mysql_pw}@{mysql_uri}:{mysql_port}/snow_report"
if not database_exists(connection_string):
	create_database(connection_string)
engine = create_engine(connection_string)
Base.metadata.create_all(engine)
session = Session(bind=engine)

@app.route("/")
def home():
	# resorts = session.query(SkiResort)
	latest_scrape = session.query(func.max(SkiResort.scrape_timestamp))
	resort = session.query(SkiResort).order_by(
		SkiResort.inches_24_hr.desc()
		).filter(and_(SkiResort.scrape_timestamp == latest_scrape,
			SkiResort.open_status == True)).first()
	# Return template and data
	return render_template("index.html", resort=resort)

@app.route("/scrape")
def scrape():
	scraped_resorts = scraper.scrape_page()
	resort_objects = []
	current_timestamp = datetime.now()
	for k, v in scraped_resorts.items():
		resort_objects.append(SkiResort(
			resort_name=k,
			open_status=v['open_status'],
			inches_24_hr=v['inches_24_hr'],
			inches_72_hr=v['inches_72_hr'],
			open_lifts_pct=v['open_lifts'],
			open_trails_pct=v['open_trails'],
			scrape_timestamp=current_timestamp
			))
	session.add_all(resort_objects)
	session.commit()

	# print(scraped_resorts)

	return redirect("/")

if __name__ == "__main__":
	app.run(debug=True)