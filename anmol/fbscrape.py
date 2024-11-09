# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time, random, datetime
import pandas as pd

'''
    Requires geckodriver, the selenium driver for Firefox browser in the same directory
    Ideally, there won't be any need of changing anything in this file, however
    if the code is not working, the most common problems can be:
    

    1. Issue in detecting an element
    --> Check xpath, css_selector or class_selector whatever is used

    2. Not able to click on element
    --> Check if any element is blocking it

    3. Internet issues
    
    If there are any other issues, please go through the functions and look for the last
    error log. Sufficient logs have been provided to identified the point of error.
    

    Note: The commented parts have been kept for debugging purpose. DO NOT REMOVE THEM

'''



class fbscrape:

    '''
    Provides utility function for scraping facebook posts and saving them as a CSV file\n
    
    Parameters:\n
    url: Takes the URL of facebook post\n
    num_posts: Numbers of posts to be scraped\n
    num_comments: Number of comments to be scraped\n
    '''

    def __init__(self, url, num_posts, num_comments):

        self.url = url
        self.num_posts = num_posts
        self.num_comments = num_comments
        self.posts = {}

    def add_sleep(self, lower, higher):

        sleep_duration = random.uniform(lower, higher)  # Adjust the range as needed
        time.sleep(sleep_duration)

    def scrape_comments(self, email, password):
        
        ''' 
            Extracts post URLs by opening them in new tabs to scrape comments through iteration and loading more
            if needed followed by cleaning data and removing null entries giving us a structured dataset\n

            Parameters:\n
            email: email-id for test account\n
            password: password for test account\n
        '''

        self.email = email
        self.password = password

        service = Service("geckodriver.exe")
        options = webdriver.FirefoxOptions()
        options.set_preference("security.ssl.enable_ocsp_stapling", False)
        options.set_preference("security.ssl.enable_ocsp_must_staple", False)
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        # options.add_experimental_option("prefs", prefs)

        #exclude logging information from console
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])

        #creating a webdriver instance
        driver = webdriver.Chrome(service= service, options= options)

        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Starting webdriver now...")
        wait = WebDriverWait(driver, 10)
        driver.get(self.url)

        # login mechanism
        # send credentials to email-id and password

        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Trying to login now...")
        try:
            email_xpath = '//*[@id="login_popup_cta_form"]/div/div[3]/div'
            email_button = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath)))
            email_box = email_button.find_element(By.TAG_NAME, "input")
            email_box.send_keys(self.email)
            

            pass_xpath = '//*[@id="login_popup_cta_form"]/div/div[4]/div'
            pass_button = wait.until(EC.presence_of_element_located((By.XPATH, pass_xpath)))
            pass_box = pass_button.find_element(By.TAG_NAME, "input")
            pass_box.send_keys(self.password)
            pass_box.send_keys(Keys.RETURN)

            self.add_sleep(4, 5)
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Logged in successfully...")


            # # click on enter
            # enter_xpath = '//*[@id="login_popup_cta_form"]/div/div[5]/div'
            # enter_button = wait.until(EC.presence_of_element_located(By.XPATH, enter_xpath))
            # enter_button.click()

        except:

            # could not login
            print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Could not login!! Trying to continue...")
        
        self.add_sleep(4, 5)

        # close the box
        # try:
        #     close_class = "x92rtbv x10l6tqk x1tk7jg1 x1vjfegm"
        #     close_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[class='{close_class}']")))
        #     close_box.click()
        # except TimeoutException:
        #     print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Close button was not found, moving on with regular operation...")

        self.add_sleep(2, 5)

        post_class = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
        n_posts = 0
        posts_list = []
        limit_posts = self.num_posts

        # check if num of posts is greater than num_posts
        # if not:
        #   scroll down
        trials = 5
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Looking for required number of posts...")

        while(True):

            posts = []
            url_flag = True

            for i in range(trials+1):
                
                if i==0:
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} URL is getting repeated! Checking if URL repeats...")
                else:
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} URL is getting repeated! Trying again... trial #{(i+1)}")


                # print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} URL is getting repeated! Trying again... trial #{(i+1)}")
                self.add_sleep(4,5)
                driver.refresh()
                self.add_sleep(4,5)

                posts = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"a[class='{post_class}']")))

                if posts[0].get_attribute('href')[:-1] == driver.current_url:
                    continue
                else:
                    url_flag = False
                    break

            if url_flag:

                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Couldn't resolve URL error after {trials} trials! Stopping...")
                return -1
            
            else:

                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Resolved URL issue! Continuing...")



            if len(posts) < limit_posts and len(posts) != n_posts:

                n_posts = len(posts)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                self.add_sleep(4, 5)

                continue

            elif len(posts) == n_posts or len(posts) >= limit_posts:

                num = min(self.num_posts, len(posts))
                posts_list = posts[:num]
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Less than {limit_posts} posts found!!")
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully extracted {num} posts...")

                break
        
        posts_list = [post.get_attribute('href') for post in posts_list]

        # go through all posts and extract comments
        for post in posts_list:

            self.posts[post] = []

        # i have extracted top 100 posts and i will open them in new tab one by one

        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Scraping comments from each posts...")

        for i, post in enumerate(posts_list):
            # open new tab
            driver.execute_script("window.open('');")

            # switch to new tab
            driver.switch_to.window(driver.window_handles[1])
            # open the link
            driver.get(post)

            # ... operations

            # extract description/caption of post
            
            descriptions = "NULL" 

            try:
                
                description_class = "x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h"

                # it is possible that there is no description given at all
                # in such a case, there will still be "description" available but NULL value
                description = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"span[class='{description_class}']")))

                # for d in description:
                    # print(d.get_attribute('innerText').strip())

                # description = [d.find_element(By.CSS_SELECTOR, f"div[dir='auto']") for d in description]

                if len(description) > 0:
                    
                    text = " "

                    for d in description:

                        caption_text = d.text.strip()
                        # print(caption_text)

                        if caption_text == '':
                            continue

                        text = text + caption_text

                    descriptions = text if text != ' ' else 'NULL'

                    # print(descriptions)
                
                if descriptions == 'NULL':
                    # if the post has no caption
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No caption found! Imputing 'NULL'...")
                else:
                    # if the post has caption
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully extracted the caption...")
            
            except EC.NoSuchElementException:
                
                # if no caption was detected because of some error
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Couldn't find description!")

            except TimeoutException:
            
                # if no caption was detected in the given time
                print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Couldn't find description!")


            # same mechanism for scraping comments as for scraping links
            # but instead of scrolling down, we click on load more button 

            # exact same mechanism as scraping links
            comments_class = "xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs"
            load_class = "div.x1i10hfl.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x3nfvp2.x1q0g3np.x87ps6o.x1a2a7pz.x6s0dn4.xi81zsa.x1iyjqo2.xs83m0k.xsyo7zv.xt0b8zv"

            n_comments = 0
            limit_comments = self.num_comments
            comments_list = []

            # EXTRACTING TIME IS DEPRECATED FOR NOW 

            # # try to scrape the time
            # time_xpath = '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div[2]/span/span/span[2]/span/a/span'

            # try:

            #     time_element = wait.until(EC.presence_of_element_located((By.XPATH, time_xpath)))
            #     print(time_element.text)

            # except TimeoutException:

            #     print("Couldn't find!")

            while(True):

                # same as above but instead of scrolling you click on view more comments
                try:

                    comments = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"div[class='{comments_class}']")))

                except TimeoutException:

                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No comment found for post {i+1}!")
                    break

                if len(comments) < limit_comments:

                    n_comments = len(comments)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

                    try:

                        load_more_button = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, load_class)))
                        driver.execute_script("arguments[0].click();", load_more_button[-1])

                    # if stale element error
                    except EC.StaleElementReferenceException:

                        continue
                    
                    # if element not found error
                    except EC.NoSuchElementException:

                        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No button found!")

                    # if timed out error
                    except TimeoutException:

                        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No \"View More Comments\" button found!")
                        num = min(self.num_comments, len(comments))
                        comments_list = comments[:num]
                        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully extracted {num} comments in post {i+1} ...")
                        break

                    self.add_sleep(4, 5)
                    continue

                # if num of comments loaded now is same as previously stored, no change OR
                # if num of comments is more than needed
                elif len(comments) == n_comments or len(comments) >= limit_comments:
                    num = min(self.num_comments, len(comments))
                    comments_list = comments[:num]
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully extracted {num} comments in post {i+1} ...")

                    break
            
            temp_comments_list = []

            for comment in comments_list:

                # try to extract comments from inner div
                try:

                    # try to catch error if comment isn't found
                    temp_comments_list.append(comment.find_element(By.TAG_NAME, "div").text.strip())

                except NoSuchElementException:

                    # display error if comment not found and impute NULL
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error occurred while extracting comment! Imputing NULL")
                    temp_comments_list.append("NULL")

                except StaleElementReferenceException:

                    # display error if comment not found and impute NULL
                    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error occurred while extracting comment! Imputing NULL")
                    temp_comments_list.append("NULL")

            # self.posts[post] = temp_comments_list

            # extend the captions into a list
            _len_ = len(temp_comments_list)
            descriptions_list = [descriptions] * _len_

            self.posts[post] = [descriptions_list, temp_comments_list]
  
            self.add_sleep(4, 5)

            # close tab
            driver.close()
            # switch back
            driver.switch_to.window(driver.window_handles[0])

        self.posts = {key: value for key, value in self.posts.items() if value}
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Successfully created dict, closing webdriver instance now...")

        # close window
        driver.quit()

    def save(self, filename):

        '''
            Saves the data from dictionary by converting the pandas 
            dataframe and into a comma-seperated file within current directory
        '''

        df = []

        # key is the post_url
        # values is [caption_list, comments_list]

        for key, values in self.posts.items():

            # values[0] is just the caption
            # values[1] is list of comments, so we iterate in that

            # print(key, values)

            for value in values[1]:

                # values[0] is the list of captions, values[0][0] is the first caption
                df.append((key, values[0][0], value))

        df = pd.DataFrame(df, columns = ['posts', 'description', 'comments'])

        filename = f"SCRAPED_{filename}.csv"
        df.to_csv(filename, index = False)
        print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Saved file as \"{filename}\" successfully...")


        