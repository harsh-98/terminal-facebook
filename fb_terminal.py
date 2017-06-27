from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyfiglet import Figlet
import selenium.webdriver
import requests
import pickle
import sys
import re
import os


class TER_fb:

   ##Initialise Driver_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

   def __init__(self):
      dcap = dict(DesiredCapabilities.PHANTOMJS)
      dcap["phantomjs.page.settings.userAgent"] = (
          "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0"    #The xpaths used in the code are with reference to the layout of m.facebook.com on Firefox Windows.
      )    
      serviceArgs = ['--load-images=no',]
      self.driver=selenium.webdriver.PhantomJS(desired_capabilities=dcap,service_args=serviceArgs)

   ##Login Functions_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

   def loginChecker(self):
      if os.path.isfile("cookies.pkl") == True:
         return True
      else:
         return False

   def login(self):
      print("Provide your credentials for login.")
      print("Credentials are not stored and required only once...")
      email = input("Email/Username/Phone : ")
      password = input("Password : ")
      
      print("Attempting Login...")
      
      self.driver.get("http://m.facebook.com/settings")
      self.driver.find_element_by_name("email").send_keys(email)
      self.driver.find_element_by_name("pass").send_keys(password + Keys.RETURN)

      dummy = 0

      try:
         if self.driver.find_element_by_xpath('//*[@id="viewport"]/div[3]/div/table/tbody/tr/td[2]/a[3]').is_displayed() == True:
            print("Successfully logged in. Dumping Cookies...")
            self.cookieDumper()
            print("Dumped Cookies")
      except NoSuchElementException:
            dummy += 1

      if dummy == 1:
         print("xxxxxxx")
         print("Unable to login, try again later.")

         

   def cookieDumper(self):                                                             #Dumps cookies on first login.
      pickle.dump(self.driver.get_cookies() , open("cookies.pkl","wb"))
      print(self.driver.get_cookies())

   def cookieInjector(self):                                                           #Injects cookies on subsequent logins.
      if os.path.isfile("cookies.pkl") == True:
         cookies = pickle.load(open("cookies.pkl", "rb"))
         self.driver.get("http://m.facebook.com")
         for cookie in cookies:
            self.driver.add_cookie(cookie)
         self.driver.get("http://m.facebook.com/settings")

   def greeting(self):
      try:
         data = self.driver.find_element_by_xpath("//*[contains(text(), 'Logout')]")
         f = Figlet(font='slant')
         self.name = re.search('\((.*?)\)',data.text).group(1) #Extracts username from 'Logout (username)' fetched from the page.
         print(f.renderText(self.name))
         self.name = self.name.lower()
      except NoSuchElementException:
            pass

   def friendWriter(self,friendList):
      if os.path.isfile("friendList.pkl") == True:
         file = open("friendList.pkl",'wb')
      else:
         print("Generating Friend List for the first time.")
         file = open("friendList.pkl",'wb')      
      pickle.dump(friendList,file)

   def home_new(self,pageNumber,click):
         if pageNumber == 0 and click == 0:
            self.driver.get("http://m.facebook.com")
            print("http://m.facebook.com")
         if click == 1:
            try:
               if pageNumber == 1:
                  self.driver.find_element_by_xpath('//*[@id="m_newsfeed_stream"]/div[3]/a').click()
               elif pageNumber > 1:
                  self.driver.find_element_by_xpath('//*[@id="root"]/div/div[3]/a').click()
            except NoSuchElementException as e :
               print(e)
               print("Cannot access the next page.")
               self.onPage = 0
            
         
         []
         try:
            path = 'div[role="article"]'
            post = self.driver.find_elements_by_css_selector(path)
            for index, i in enumerate(post):
               #print(i.get_attribute("innerHTML"))
               #re.(i)
               try:
                  print("\n\n---{}---\n{}".format(index,self.render(i.text)))
               except (UnicodeDecodeError,UnicodeEncodeError) as e:
                  print(e)
         except NoSuchElementException as e:
            print(e)
         print("xxxxxxx")

   def render(self,post):
      post = re.sub('. Add Friend . Full Story . More',' ',post)                        #Replaces irrelevent text with ''
      post = re.sub('Add Friend\n','',post)
      post = re.sub('. Full Story . More','',post)
      post = re.sub('. Like Page','',post)
      post = re.sub('Like Page . More','',post)
      post = re.sub('. Share','',post)
      post = re.sub('More','',post)
      post = re.sub('. More','',post)
      post = re.sub('Share','',post)
      post = re.sub('Join Page','',post)
      post = re.sub('Like Page','',post)
      post = re.sub('Join Event','',post)

      return post

   def notify(self):
      try:
         self.driver.get("https://m.facebook.com/notifications")
         temp = self.dateCurator()
         dates = temp[0]
         xpaths = temp[1]
         print("\nxxxxxxx\nNotifications\nxxxxxxx\n")
         for index,date in enumerate(dates):
            print(date + ":")
            notifications = self.getNotifications(xpaths[index])
            for notification in notifications:
               print("- - - - -")
               print(notification)
            print("x_x_x_x_x_x_x_x_x_x")
      except NoSuchElementException:
         print("xxxxxxx\nCannot Print Notifications\nxxxxxxx")


   def friendWriter(self,friendList):
      if os.path.isfile("friendList.pkl") == True:
         file = open("friendList.pkl",'wb')
      else:
         print("Generating Friend List for the first time.")
         file = open("friendList.pkl",'wb')      
      pickle.dump(friendList,file)

   def friendList(self):
      holder = []
      n = 0
      dummy = 0
      
      print("Fetching Friend List",end='')

      while n <= 500:
         print(".",end='')
         sys.stdout.flush()
         try:
            self.driver.get("https://m.facebook.com/friends/center/friends/?ppk={}".format(n))
            a = 1
            while a<= 10:
               element = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[{}]/table/tbody/tr/td[2]/a'.format(a))
               holder.append(element.text + "," + element.get_attribute("href").split('/')[6].split('&')[0].split('?uid=')[1])
               a += 1
            n += 1
         except NoSuchElementException:
            try:
               elem = self.driver.find_element_by_xpath('//*[@id="friends_center_main"]/div[2]/div[1]/table/tbody/tr/td[2]/a')
               n += 1
            except:
               break

      print("")    
      return holder

   def manager(self,command):
    if command == "exit":
         sys.exit()
    elif command == "new":
         self.home_new(0,0)
    elif command == "notif":
         self.notify()
    elif command == "auli":
         self.friendLiker()

    self.commandInput()

   def commandInput(self):
      print("")
      print("Use 'help' to get the list of commands. Use 'exit' to logoff.")
      command = input("Enter command : ")
      self.manager(command)

def main():

   tool = TER_fb()
   f = Figlet(font='slant')
   print(f.renderText('TER_fb\n------'))
   
   if tool.loginChecker() == True:
      print("Attempting Login...")
      tool.cookieInjector()
   else:
      tool.login()

   if tool.loginChecker() == True:
      tool.greeting()
      tool.commandInput()
   else:
      sys.exit("Can't proceed.")

if __name__ == "__main__":main()