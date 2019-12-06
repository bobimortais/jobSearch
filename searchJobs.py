import requests
import json

def printLinkedInJobs(jobs):
	for index in range(1, len(jobs)):
		jobTitle = jobs[index].split('job-result-card__title">')[1].split('<')[0]
		company = jobs[index].split('job-result-card__subtitle-link')[1].split('>')[1].split('<')[0]
		location = jobs[index].split('job-result-card__location">')[1].split('<')[0]
		jobLink = 'http://linkedin.com/jobs/view/' + jobs[index].split('data-id="')[1].split('"')[0]
		timePosted = jobs[index].split('job-result-card__listdate')[1].split('>')[1].split('<')[0]
		print('Title: ' + jobTitle)
		print('Company: ' + company)
		print('Location: ' + location)
		print('Time Posted: ' + timePosted)
		print('Job Link: ' + jobLink)
		print('\n')
		
def printLandingJobsJobs(jobs):
	for job in jobs:
		print('Title: ' + job['title'])
		print('Company: ' + job['company_name'])
		print('Location: ' + job['location'])
		print('Time Posted: ' + job['published_at'])
		print('Job Link: ' + job['url'])
		print('\n')
		
def searchJobsFromURL(url):
	URL = url
	r = requests.get(url = URL)
	responseTOString = str(r.text)
	return responseTOString

#Linkedin
responseTOString = searchJobsFromURL('https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=103644278&keywords=remote%20java%20developer&location=United%20States&originalSubdomain=br')
jobs = responseTOString.split('result-card job-result-card')
printLinkedInJobs(jobs)

#LandingJobs
responseTOString = searchJobsFromURL('https://landing.jobs/jobs/search?page=1&remote=true&hd=false&t_co=false&t_st=false')
jsonReponse = json.loads(responseTOString)
jobs = jsonReponse['offers']
printLandingJobsJobs(jobs)
	
