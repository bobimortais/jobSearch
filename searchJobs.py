import requests
import json

#URLs to Search
linkedInURL = 'https://www.linkedin.com/jobs/search/?keywords=remote%20java%20developer&location=Netherlands'
landingJobsURL = 'https://landing.jobs/jobs/search?page=1&remote=true&hd=false&t_co=false&t_st=false'
moberriesURL = 'https://www.moberries.com/jobs-search?q=remote&category=1'
jobliftURL = 'https://joblift.com/Jobs-for-remote%20software-the-last-7-days'

def getLinkedInJobs(jobs):
	formattedJobs = []
	for index in range(1, len(jobs)):
	
		try:
			jobTitle = jobs[index].split('job-result-card__title">')[1].split('<')[0]
			company = jobs[index].split('job-result-card__subtitle-link')[1].split('>')[1].split('<')[0]
			location = jobs[index].split('job-result-card__location">')[1].split('<')[0]
			jobLink = 'http://linkedin.com/jobs/view/' + jobs[index].split('data-id="')[1].split('"')[0]
			timePosted = jobs[index].split('job-result-card__listdate')[1].split('>')[1].split('<')[0]
			newJob = {"title" : jobTitle, "company" : company, "location" : location, "joblink" : jobLink, "timePosted" : timePosted}
			formattedJobs.append(newJob)
		except:
			print('Error parsing response for linkedIn Job\n')
	return formattedJobs
		
def getLandingJobsJobs(jobs):
	formattedJobs = []
	for job in jobs:
		newJob = {"title" : job['title'], "company" : job['company_name'], "location" : job['location'], "joblink" : job['url'], "timePosted" : job['published_at']}
		formattedJobs.append(newJob)
	return formattedJobs
		
def getMoberriesJobs(jobs):
	formattedJobs = []
	jobs = jobs.split('media">')
	for index in range(1, len(jobs)):
		try:
			jobTitle = jobs[index].split('<a')[1].split('>')[1].split('<')[0]
			company = jobs[index].split('span>')[1].split('<')[0]
			location = jobs[index].split('tag-list">')[1].split('</i>')[1].split('</span>')[0].split('>')[1]
			jobLink = 'https://www.moberries.com/job/' + jobs[index].split('/job/')[1].split('"')[0]
			newJob = {"title" : jobTitle, "company" : company, "location" : location, "joblink" : jobLink, "timePosted" : ""}
			formattedJobs.append(newJob)
		except:
			print('Error parsing response for Moberries job\n')

	return formattedJobs
	
def getJobliftJobs(jobs):
	formattedJobs = []
	jobs = jobs.split('jobItem">')
	for index in range(1, len(jobs)):
		try:
			jobTitle = jobs[index].split('jobTitleLink')[1].split('>')[1].split('<')[0]
			company = jobs[index].split('job__infos">')[1].split('<span>')[1].split('<')[0]
			location = jobs[index].split('job__infos">')[1].split('</span>')[1].split('>')[1]
			jobLink = 'https://joblift.com' + jobs[index].split('jobLink')[1].split('href="')[1].split(';')[0]
			newJob = {"title" : jobTitle, "company" : company, "location" : location, "joblink" : jobLink, "timePosted" : ""}
			formattedJobs.append(newJob)
		except:
			print('Error parsing response for Joblift job\n')
	return formattedJobs
		
def getDetailsFromJobsLinkedIn(formattedJobs):
	for index in range(0, len(formattedJobs)):
		try:
			currentJob = json.loads(json.dumps(formattedJobs[index]))
			
			if 'linkedin' not in currentJob['joblink']:
				continue
				
			jobUrl = currentJob['joblink']
			jobDescription = searchJobsFromURL(jobUrl)
			jobDescription = jobDescription.split('description__text--rich')[1].split('</section>')[0]
			
			if 'remote' in jobDescription.lower():
				print('======Interesting job======')
				print('Title: ' + currentJob['title'])
				print('Company: ' + currentJob['company'])
				print('Location: ' + currentJob['location'])
				print('Job Link: ' + jobUrl)
				print('\n')
		except:
			print('Error parsing response for LinkedIn job\n')
			
def printJobsInfo(formattedJobs):
	for index in range(0, len(formattedJobs)):
		currentJob = json.loads(json.dumps(formattedJobs[index]))
		print('Title: ' + currentJob['title'])
		print('Company: ' + currentJob['company'])
		print('Location: ' + currentJob['location'])
		print('Time Posted: ' + currentJob['timePosted'])
		print('Job Link: ' + currentJob['joblink'])
		print('\n')
		
def searchJobsFromURL(url):
	URL = url
	r = requests.get(url = URL)
	responseTOString = str(r.text)
	return responseTOString

userOption = int(input("Welcome to the job search. Which option do you want: \n1 - Show all jobs \n2 - Show only jobs with specific description\n"))

formattedJobs = []
#Linkedin
responseTOString = searchJobsFromURL(linkedInURL)
jobs = responseTOString.split('result-card job-result-card')
formattedJobs.extend(getLinkedInJobs(jobs))

#LandingJobs
responseTOString = searchJobsFromURL(landingJobsURL)
jsonReponse = json.loads(responseTOString)
jobs = jsonReponse['offers']
formattedJobs.extend(getLandingJobsJobs(jobs))

#Moberries
responseTOString = searchJobsFromURL(moberriesURL)
jobs = responseTOString.split('job-list')[1]
formattedJobs.extend(getMoberriesJobs(jobs))

#Joblift
responseTOString = searchJobsFromURL(jobliftURL)
jobs = responseTOString.split('searchresult__resultlist">')[1]
formattedJobs.extend(getJobliftJobs(jobs))

if userOption == 1:
	printJobsInfo(formattedJobs)
#Implemented only for LinkedIn jobs
elif userOption == 2:
	getDetailsFromJobsLinkedIn(formattedJobs)
	