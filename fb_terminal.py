from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from pyfiglet import Figlet
import selenium.webdriver


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