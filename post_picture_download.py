import os
from skimage import io
from crawlerforpost import CrawlerForPosts


def save_img(img_url, file_path):
    flag = True
    try:
        image = io.imread(img_url)
        try:
            io.imsave(file_path, image)
        except (UnboundLocalError, KeyError, IOError, ValueError):
            print('[错误]当前图片无法保存')
            flag = False
    except (OSError, KeyError, IOError):
        print('[错误]当前图片无法链接')
        flag = False
    return flag


def save_img_list(global_set):
    save_path = global_set.save_dir_path
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    index = 0
    for img_url in global_set.img_url_list:
        if img_url:
            index += 1
            print('>>> >>> ' + str(index), end="")
            file_path = global_set.save_dir_path + str(index) + img_url[-4:]
            print(' > ', end="")
            flag = save_img(img_url, file_path)
            if flag:
                global_set.download_number += 1
                print('Success!')
                global_set.total_d_pic_num += 1


def post_main(start_url, global_set):
    #  设置参数 ========================================================================================================
    target_url = start_url
    global_set.img_url_list = []
    #  创建爬虫
    crawler = CrawlerForPosts(target_url)
    #  抓取页面图片链接 ================================================================================================
    while (crawler.next_pag != "") & (global_set.now_pag_number < global_set.max_pag_number):
        #  显示开始抓取信息
        global_set.now_pag_number += 1
        print('>>> >>> ' + 'page ' + str(global_set.now_pag_number) + ' start scan ...')
        #  抓取信息
        crawler.get_info()
        global_set.img_url_list += crawler.img_url_list
        #  显示抓取结果
        print('>>> >>> ' + str(len(crawler.img_url_list)) + ' images has been find.')
    #  开始保存抓取图片 ================================================================================================
    pic_number = len(global_set.img_url_list)
    if pic_number:
        print('>>> >>> ' + str(pic_number) + ' images begin download ...')
        save_img_list(global_set)
        print('>>> >>> ' + str(global_set.download_number) + ' images has been download.')
    #  结束  ===========================================================================================================



