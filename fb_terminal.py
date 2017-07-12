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

   def dateCurator(self):
      dates = []
      xpaths = []
      n = 1
      while n < 10:
         try:            
            xpath = '//*[@id="notifications_list"]/div[{}]/h5'.format(n)
            date = self.driver.find_element_by_xpath(xpath).text
            dates.append(date)
            xpaths.append(xpath)
            n += 1
         except NoSuchElementException:
            n += 1
            break
      return [dates,xpaths]

   def getNotifications(self,basepath):
      notifications = []
      n = 1
      while n < 20:
         try:            
            xpath = re.sub("/h5",'',basepath)+"/div[{}]/table/tbody/tr/td[2]/a/div".format(n)
            notification = self.driver.find_element_by_xpath(xpath).text
            notifications.append(notification)
            n += 1
         except NoSuchElementException:
            n += 1
            break
      return notifications


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


   def friendLiker(self, index_=0):
      print("THIS WILL LIKE EACH AND EVERY POST OF A SPECIFIED FRIEND.")
      print("ENTER 'p' TO PROCEED OR ANYTHING ELSE TO QUIT.")
      choice = input("")
      if choice == 'p' or choice == 'P':
         if os.path.isfile("friendList.pkl") == False:
            print("Friend List not found.")
            print("Use 'unfr' first to get the initial friend list.")
            return False
         else:
            print("\nxxxxxxx\nIndex : Friend (alphabetical order):\nxxxxxxx")
            file = pickle.load(open("friendList.pkl",'rb'))
            for index,line in enumerate(sorted(file)):
               print(str(index)+" : "+line.split(',')[0])
            print("\nxxxxxxx\nEnter Index\nxxxxxxx")
            index = input("Index: ")


            if index.isdigit() and index_==0:
               self.loadProfile(int(index))
            elif index.isdigit() and index_==1:
               print("loading")

               self.friendProfile(int(index), index_)

            else:
               print("Invalid Index")
      else:
         return False

   def friendProfile(self, number, index_=0):
      uid = 0
      for index,line in enumerate(sorted(pickle.load(open("friendList.pkl",'rb')))):
         if index == number:
            uid = int(line.split(',')[1])
            print("Liking all posts on {}'s Timeline...".format(line.split(',')[0].split()[0]))
            break
      print(uid)
      if index_==1:
         try:
            self.driver.get("http://m.facebook.com/messages/thread/{}/?refid=17&__xt__=48.%7B%22event%22%3A%22message%22%2C%22intent_status%22%3Anull%2C%22intent_type%22%3Anull%2C%22profile_id%22%3A{}%2C%22ref%22%3A3%7D".format(uid, uid))
            comment = input("Enter your comment:\n")
            no = input("Enter the number of times the comment is to be printed : ")
            for i in range(int(no)):
              a= self.driver.find_element_by_xpath('//*[@id="composerInput"]') 
            a.send_keys(comment)
            self.driver.find_element_by_xpath('//input[@value="Send"]').click()
            print("Commented.")
         except Exception as e:
            print("Unable to comment.")
            print(e)
         
      else:
         self.driver.get("http://m.facebook.com/{}".format(uid))

   def loadProfile(self,number):
      self.friendProfile(number)
      try:       
         temp = self.elementYear()
         years = []
         names = []
         numberOfLikes = 0
         alreadyLiked = 0
         totalLiked = 0
         totalAlreadyLiked = 0
         for x in temp:
            years.append(x.get_attribute("href"))
            names.append(x.text)
         print(names)
         print(years)
        # sys.exit(0)
         print("*one '.' == 1 Like Administered*")
         for index,year in enumerate(years):
            self.driver.get(year)
            if index != 0:
               stories = self.allStories()
               print("\nstories\n")
               print(stories)
            else:
               stories = "dummyValue"
            print("\nxxxxxxx {} xxxxxxx".format(names[index]))
            if stories != None:
               if stories != "dummy":
                  self.driver.get(stories)
                  showmorelink = self.showMore()
                  while showmorelink != "dummy":
                     print("\nshowmorelinks\n")
                     print(showmorelink)
                     likelinks = self.friendLikeLink()
                     print("\nlinkLinks\n")
                     print(likelinks)
                     alreadyLiked += likelinks[0]
                     totalAlreadyLiked += likelinks[0]
                     likedJustNow = self.likeAllLinks(likelinks[1])
                     numberOfLikes += likedJustNow
                     totalLiked += likedJustNow
                     self.driver.get(showmorelink)
                     showmorelink = self.showMore()
                  if showmorelink == "dummy":
                     likelinks = self.friendLikeLink()
                     alreadyLiked += likelinks[0]
                     totalAlreadyLiked += likelinks[0]
                     likedJustNow = self.likeAllLinks(likelinks[1])
                     numberOfLikes += likedJustNow
                     totalLiked += likedJustNow
                  print("\nPosts liked now: {}".format(numberOfLikes))
                  print("Posts already liked: {}".format(alreadyLiked))
                  numberOfLikes = 0
                  alreadyLiked = 0
               else:
                  print("Failed")
            if stories == None:
               likelinks = self.friendLikeLink()
               alreadyLiked += likelinks[0]
               totalAlreadyLiked += likelinks[0]
               likedJustNow = self.likeAllLinks(likelinks[1])
               numberOfLikes += likedJustNow
               totalLiked += likedJustNow               
               print("\nPosts liked now: {}".format(numberOfLikes))
               print("Posts already liked: {}".format(alreadyLiked))
               numberOfLikes = 0
               alreadyLiked = 0
         print("\nxxxxxxx REPORT xxxxxxx\n")
         print("Total Likes Administered Now: {}".format(totalLiked))
         print("Number Of Already Liked Posts: {}".format(totalAlreadyLiked))
         print("Total Likes on Friend's Timeline: {}".format(totalLiked + totalAlreadyLiked))       
      except NoSuchElementException:
         print("Can't Proceed")

   def allStories(self):
      link = ""      
      try:
         showall = self.driver.find_elements_by_xpath("//*[contains(text(), 'Show all stories')]")
         for show in showall:
            if self.checkValidLink(show,"stories") == True:
               link = show.get_attribute("href")
               return link
            else:
               return "dummy"
      except NoSuchElementException:
         return "dummy"

   def showMore(self):
      try:
         showmore = self.driver.find_element_by_xpath("//*[contains(text(), 'Show more')]")
         if self.checkValidLink(showmore,"showmore") == True:
            return showmore.get_attribute("href")
         else:
            return "dummy"
      except NoSuchElementException:
         return "dummy"
                    

   def checkValidLink(self,temp,user):
      if user == "stories":
         try:
            link = temp.get_attribute("href")      
            if link.split('/')[2] == "m.facebook.com":
               return True
            else:
               return False
         except:
            return False
      elif user == "likes":
         try:
            link = temp.get_attribute("href")
            if link.split('/')[2] == "m.facebook.com":
               if "like.php" in link:
                  return True
               else:
                  return False
         except:
            return False
      elif user == "showmore":
         try:
            link = temp.get_attribute("href")
            if link.split('/')[2] == "m.facebook.com":
               return True
            else:
               return False
         except:
            return False           
      else:
         return False

      
   def elementYear(self):
      n = 1
      holder = []
      while n < 20:
         try:
            holder.append(self.driver.find_element_by_xpath('//*[@id="structured_composer_async_container"]/div[4]/div[{}]/a'.format(n)))
            n += 1
         except NoSuchElementException:
            break
      if holder == []:
         n = 1
         while n < 20:
            try:
               holder.append(self.driver.find_element_by_xpath('//*[@id="structured_composer_async_container"]/div[3]/div[{}]/a'.format(n)))
               n += 1
            except NoSuchElementException:
               break
      return holder

   def friendLikeLink(self):
      holder = []
      try:
         likeLinks = self.driver.find_elements_by_xpath("//*[contains(text(), 'Like')]")
         print("\nfriend\n")
         print(likeLinks)
         unlikeLinks = self.driver.find_elements_by_xpath("//*[contains(text(), 'Unlike')]")
         print("\nunfriend\n")
         print(unlikeLinks)
         for like in likeLinks:
            if self.checkValidLink(like,"likes") == True:
               holder.append(like.get_attribute("href"))
         alreadyLiked = len(unlikeLinks)
         return [alreadyLiked,holder]
      except NoSuchElementException:
         return []

   def likeAllLinks(self,links):
      file = pickle.load(open("cookies.pkl",'rb'))
      numberOfLikes = 0
      cookies = {}
      for x in file:
         if 'datr' in str(x):
           cookies["datr"] = x["value"]
         if 'xs' in str(x):
           cookies["xs"] = x["value"]
         if 'c_user' in str(x):
           cookies["c_user"] = x["value"]
      for link in links:
         r = requests.get(link,cookies = cookies)
         if r.status_code == 200:
            print(".",end = '')
            sys.stdout.flush()
            numberOfLikes += 1
         else:
            print("Failed")
      return numberOfLikes

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