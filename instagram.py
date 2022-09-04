# Gerekli olan kütüphaneleri import ettik
from re import search
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

#Class açtık
class Instagram:
    def __init__(self,username,password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password
        
# Giriş yapmak için fonksiyon yazdık
    def singIn(self):
        
        self.browser.get("https://www.instagram.com/accounts/login/")
        
        time.sleep(3)
        
# Ekranı Full screen yaptık
        self.browser.maximize_window()
        
        time.sleep(3)
        
        username1 = self.browser.find_element(By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input")
        Password1 = self.browser.find_element(By.XPATH , "//*[@id='loginForm']/div/div[2]/div/label/input")
        username1.send_keys(self.username)
        Password1.send_keys(self.password)
        
        time.sleep(3)
        
        giris_yap = self.browser.find_element(By.XPATH , "//*[@id='loginForm']/div/div[3]/button")
        giris_yap.click()
        
        time.sleep(3)
        
# Takipçiler kısmına girmek için fonksiyon 
    def getFollowers(self):
        self.browser.get(f"https://www.instagram.com/{self.username}/followers/")
        
        time.sleep(3)
        
# JsKomut yerini burada çalıştırdık aşağıda açıklayacağım
        Instagram.scrolldown(self)
        
        followerList = []
        
# Burada takipçileri aldık "1 yazdığım yer ile " ardından for döngüsü ile tek tek yazdırdık
        takipciler = self.browser.find_elements(By.CSS_SELECTOR, " ._ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm") #1
        sayac = 0
        for takipci in takipciler:
            sayac += 1
            print(str(sayac) + "-->" + takipci.text)
            followerList.append(takipci.text) # Listeye kaydettik
            
# Dosya açtık ve for döngüsü ile dosyaya yazdırdık
        with open("followers.txt" , "w" , encoding="UTF-8") as file:
            for item in followerList:
                file.write(str(item) + "\n")
                
        time.sleep(3)
        
# Takip ettiklerimi almak için fonksiyon açtım
    def getFollow(self):
        self.browser.get(f"https://www.instagram.com/{self.username}/following/")
        
        time.sleep(3)
        
# JavaScript kullandım üstteki gibi
        Instagram.scrolldown(self)
        
# Listeyi oluşturdum
        followList = []
        
# Üstekinin aynısını yapıyorum sadece takip edilenleri alıyoruz tek farkı o
        takipedilenler = self.browser.find_elements(By.CSS_SELECTOR, "._ab8y._ab94._ab97._ab9f._ab9k._ab9p._abcm")
        sayac2= 0 
        for takip in takipedilenler:
            sayac2 += 1
            print(str(sayac2) + "-->" + takip.text)
            followList.append(takip.text)
            
# Yeni bir dosya açtım ve yazdırdım
        with open("following.txt" , "w" , encoding="UTF-8") as file:
            for item2 in followList:
                file.write(str(item2) + "\n")
            
# Burada JavaScript Kullandık 
    def scrolldown(self):
        jsKomut = """ 
        sayfa = document.querySelector("._aano");
        sayfa.scrollTo(0,sayfa.scrollHeight);
        var sayfaSonu = sayfa.scrollHeight;
        return sayfaSonu;
        """
        
# Burada diğer fonksiyonlarada kullanmak için kod yazdık üstte kullandığımız yer falan buradan karışık biraz kısaca scrollu aşağı çekmek için döngü sağladık en aşağıya geldiğinde dur dedik.
        sayfaSonu = self.browser.execute_script(jsKomut)
        while True:
            son = sayfaSonu
            time.sleep(1)
            sayfaSonu = self.browser.execute_script(jsKomut)
            if son == sayfaSonu:
                break
        
# Burada Takip ettiğiniz Ama sizi takip etmeyen kişileri yazdırması için fonksiyon yazdık
    def denkmi(self):
            file_followers = open("followers.txt" , "r+" , encoding="UTF-8")
            file_followers_read = file_followers.readlines()
            file_followers_readed = [x[:-1] for x in file_followers_read]

            file_following = open("following.txt" , "r+" , encoding="UTF-8")
            file_following_read = file_following.readlines()
            file_following_readed = [x[:-1] for x in file_following_read]
            
            with open("TakipEtmeyenler.txt" , "w" , encoding="UTF-8") as file:
                    for i in file_following_readed:
                        if i not in file_followers_readed:
                                file.write("Takip Etmiyor -->" + " " + str(i) + "\n")
                        else:
                                continue
            
# Kullanıcıdan veri aldık
username = input("Kullanıcı Adınızı Giriniz: ")   
password = input("Parolanızı Giriniz: ")   

# Fonksiyonu Çalıştırdık
instgrm = Instagram(username,password)
instgrm.singIn()
instgrm.getFollowers()
instgrm.getFollow()
instgrm.denkmi()