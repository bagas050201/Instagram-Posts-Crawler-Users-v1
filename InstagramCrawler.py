from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import emoji
import string
import csv
import os

def getFileSize(nameFile):
    return os.stat(nameFile).st_size

browser = webdriver.Chrome()

def loginInstagram(url, username, password):
    browser.get(url) #Masuk ke url.
    time.sleep(2) #Memberi kesempatan untuk loading page.
    browser.find_element_by_xpath('/html/body/span/section/main/article/div[2]/div[2]/p/a').click() #Click untuk ke halaman login.
    #3 baris ke bawah berfungsi untuk mengisi form dan login.
    print("Mengisi form login ....")
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(username)
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(password)
    browser.find_element_by_xpath('/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]/button').click()
    time.sleep(3) #Memberi kesempatan untuk loading page.
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[3]/button[2]').click() #Menutup pop-up yang muncul.
    browser.find_element_by_xpath('/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]/a/span').click() #Menuju ke halaman profile user.

def getListFollowers(username, jml_followers = 0):
    print("Sedang mengload data daftar followers " + username + " ....")
    time.sleep(3) #Untuk menunggu page profile home selesai diload
    if jml_followers == 0:
        jml_followers = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title') #Untuk mendapatkan jumlah followers users di dalam list
        jml_followers.replace(',','')
    browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a').click() #Meng-click href untuk melihat tampilan followersnya
    time.sleep(2)
    followersList = browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul')
    lengthListFollowers = len(followersList.find_elements_by_css_selector('li')) #Untuk mendapatkan panjang list followers yang sudah ditampilkan
    time.sleep(2)
    followersList.click()#klik bar kosong akun pertama
    actionChain = webdriver.ActionChains(browser) #Mengambil ActionChains
    daftar = []
    nilai_berulang = 0
    batas_berulang = 0

    while lengthListFollowers < int(jml_followers) and lengthListFollowers < 200:
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li[' + str(lengthListFollowers-2) + ']').click() #Supaya bisa ngescroll sampai batas yang ditentukan
        actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
        if nilai_berulang == lengthListFollowers:
            batas_berulang += 1
            if batas_berulang == 4:
                break
        else:
            batas_berulang = 0
        nilai_berulang = lengthListFollowers
        lengthListFollowers = len(browser.find_elements_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li'))

    for i in range(1,lengthListFollowers+1):
        if int(jml_followers) > 12:
            daftar.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(i)+']/div/div[1]/div[2]/div[1]/a').get_attribute('title'))
        else:
            daftar.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[2]/ul/div/li['+str(i)+']/div/div[2]/div[1]/div/div/a').get_attribute('title'))
    return daftar

def writeToCSVandGTF(index, username, namafile): #GTF = Get Total Followers from target, GTF berguna untuk penentuan target selanjutnya.
    print('Sedang Crawling target ' + username + ' ....')
    try:
        browser.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[1]/div/h2') #Ngecek private atau ngga, kalau ngga private lanjut ke except
        return 0, index
            
    except:
        time.sleep(2)
        translator = str.maketrans('', '', string.punctuation) #Untuk ngebuat teksnya rapih
            
        def give_emoji_free_text(text): #Untuk membuang semua emoji
            allchars = [str for str in text.encode('ascii', 'ignore').decode('utf-8')]
            emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
            clean_text = ' '.join([str for str in text.encode('ascii', 'ignore').decode('utf-8').split() if not any(i in str for i in emoji_list)])
            return clean_text

        def hashtag(text): #Untuk mendapatkan tag
            char = text.encode('ascii', 'ignore').decode('utf-8').replace('\n',' ')
            tag = []
            teks = ''
            tulis = 0
            for i in range(len(char)):
                if tulis == 1:
                    teks = teks + char[i]
                if char[i] == '#':
                    tulis = 1
                elif (char[i] == ' ' or i == len(char)-1) and teks != '':
                    teks = '#' + teks
                    tag.append(teks)
                    tulis = 0
                    teks = ''
            return tag
        
        jml_followers = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[2]/a/span').get_attribute('title') #Untuk mendapatkan total followers target
        jml_posts = browser.find_element_by_xpath('/html/body/span/section/main/div/header/section/ul/li[1]/span/span').text #Untuk mendapatkan total posts target
        jml_followers = jml_followers.replace(',','')
        jml_posts = jml_posts.replace(',','')

        if int(jml_posts) == 0:
            return int(jml_followers), index
        
        tes = 0
        galat = 0
        benar = 1
        while benar == 1 and int(jml_posts) != 0:
            try:
                browser.find_element_by_xpath('/html/body/span/section/main/div/div['+str(tes)+']/article/div[1]/div/div[1]/div[1]').click()
                benar = 0
            except:
                tes += 1
                galat += 1
                if galat == 10:
                    break
                continue
                
        time.sleep(1)

        #Crawling post
        limit = 0
        while limit < int(jml_posts)-1 and int(jml_posts) != 0 and galat != 11:
            #print("Sedang crawling data posts target " + username + " ....")
            loading = False
            kanan = False
            kiri = False
            try:
                time.sleep(3)
                browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/svg')
                if limit > 0:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                    loading = True
                    kanan = True
                else:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                    loading = True
                    kiri = True
                    
            except:
                try:
                    ### Ini jika ada bulet-buletan loading
                    if loading:
                        if kiri:
                            time.sleep(2)
                            browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                            loading = False
                            kiri = False
                            continue
                        elif kanan:
                            time.sleep(2)
                            browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a[2]').click()
                            loading = False
                            kanan = False
                            continue                        
                    ### Sampai sini lalu hasilnya akan dikontinue ke awal, untuk ngambil pos yang sebelumnya muter-muter
                        
                    teks = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span').text #Mengambil captionnya dan menyimpannya dalam variabel teks
                    tag = hashtag(teks) #Meyimpan kumpulan tag
                    if len(tag) == 0:
                        tag = ''
                    teks = give_emoji_free_text(teks) #Menyingkirkan emoji dari teks
                    teks = teks.translate(translator).lower() #Membuat huruf menjadi kecil
                except:
                    teks = ''
                    tag = ''
                    
                try:
                    try:
                        likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span').text #Untuk mengambil like yang punya banyak likes.
                    except:
                        likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button').text #Untuk likes-nya sedikit
                        likes = likes.replace('like this','').replace('like','')#Untuk me-replace 'like this' atau 'like'
                except:
                    likes = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/span/span').text #Untuk mendapatkan likes dari video
                #print(teks, likes, tag)

                try:
                    commentlist = len(browser.find_elements_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul')) #panjang dari banyak komen
                    comment = []
                    ##print(commentlist)
                    for i in range(1,commentlist+1):
                        morecomment = []
                        commentter = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/h3/a').text
                        teksc = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul['+str(i)+']/div/li/div/div[1]/div[2]/span').text
                        teksc = give_emoji_free_text(teksc)
                        teksc = teksc.translate(translator).lower()
                        morecomment.append(commentter)
                        morecomment.append(teksc)
                        comment.append(morecomment)
                        #print(commentter,teks)
                    if len(comment) == 0:
                        comment = ''
                except:
                    comment = ''

                if index == 0:
                    with open(namafile,'a',newline='') as csvfile: #Membuka dan membuat file '.csv'
                        writer = csv.writer(csvfile)
                        writer.writerow(['username','post','tag','likes','comment'])
                        writer.writerow([username, teks, tag, likes, comment])
                    index += 1
                else:
                    with open(namafile, 'a', newline = '') as csvfile: #Menambahkan file '.csv' dengan data baru
                        writer = csv.writer(csvfile)
                        #print(username, teks, tag, likes, comment)
                        writer.writerow([username, teks, tag, likes, comment])
                    index += 1
                    
                if limit == 0:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a').click()
                else:
                    browser.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/a[2]').click()
                    
                #print()
                time.sleep(2)
                limit += 1      
    return int(jml_followers), index
    
def mulaiProgram(url, username, password):
    loginInstagram(url, username, password)
    hitung = 0
    sizeOfFile = 0
    namafile = input("Masukkan nama file: ")
    namafix = namafile+'.csv'
    while sizeOfFile < 1024*1024*100:
        tertinggi = 0
        indekss = 0
        try:
            listTotalFollowersFromTarget = []
            listFollowers = []
            listFollowers = getListFollowers(username, tertinggi)
            #print(listFollowers)
                        
            for usertarget in listFollowers:
                browser.get(url+'/'+usertarget)
                time.sleep(3)
                totalFollowers, indekss = writeToCSVandGTF(indekss, usertarget,namafix)
                listTotalFollowersFromTarget.append(totalFollowers)
                hitung += 1

            #print( listTotalFollowersFromTarget )      
            tertinggi = max(listTotalFollowersFromTarget)
            #print(tertinggi)
            indeks = listTotalFollowersFromTarget.index(tertinggi)
            #print(indeks)
            browser.get(url+'/'+username)
            time.sleep(2)
            username = listFollowers[indeks]
            #print(username)      
            browser.get(url+'/'+username)
                
        except:
            continue
    sizeOfFile = getFileSize(namafix)
                
user = input('Masukkan username akun anda: ')
passwo = input('Masukkan password akun anda: ')

url = 'https://www.instagram.com'
username = user
password = passwo

mulaiProgram(url, username, password)
browser.quit()
