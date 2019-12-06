import requests
import json

#URLs to Search
linkedInURL = 'https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=103644278&keywords=remote%20java%20developer&location=United%20States&originalSubdomain=br'
landingJobsURL = 'https://landing.jobs/jobs/search?page=1&remote=true&hd=false&t_co=false&t_st=false'
moberriesURL = 'https://www.moberries.com/jobs-search?q=remote&category=1'


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
		
def printMoberriesJobs(jobs):
	jobs = jobs.split('media">')
	for index in range(1, len(jobs)):
		jobTitle = jobs[index].split('<a')[1].split('>')[1].split('<')[0]
		company = jobs[index].split('span>')[1].split('<')[0]
		location = jobs[index].split('tag-list">')[1].split('</i>')[1].split('</span>')[0].split('>')[1]
		jobLink = 'https://www.moberries.com/job/' + jobs[index].split('/job/')[1].split('"')[0]
		print('Title: ' + jobTitle)
		print('Company: ' + company)
		print('Location: ' + location)
		print('Job Link: ' + jobLink)
		print('\n')
	
		
def searchJobsFromURL(url):
	URL = url
	r = requests.get(url = URL)
	responseTOString = str(r.text)
	return responseTOString

#Linkedin
responseTOString = searchJobsFromURL(linkedInURL)
jobs = responseTOString.split('result-card job-result-card')
printLinkedInJobs(jobs)

#LandingJobs
responseTOString = searchJobsFromURL(landingJobsURL)
jsonReponse = json.loads(responseTOString)
jobs = jsonReponse['offers']
printLandingJobsJobs(jobs)

#Moberries
responseTOString = searchJobsFromURL(moberriesURL)
jobs = responseTOString.split('job-list')[1]
printMoberriesJobs(jobs)