if __name__ == "__main__":
   # page = 8
    url = "http://www.mmjpg.com/"

    base_url = urlparse(url)
    #url = "http://cuiqingcai.com/1319.html"
    #menu = getallAltls(url)
    ##menu = getparAltls(url, page)

    #url = "http://www.mmjpg.com/tag/tgod"
    path =  r"E:\image"
    #path = path + "\\" + "推女神"
    craw = Crawler()
    soup = craw.doc(craw.getHtml(url))
    total = 0
    for each in soup(soup(".subnav")('a[href^="http://www.mmjpg.com/tag"]')).items():
        utils.log( "即将下载： " + each.text() + each.attr('href') )
        path= r"E:\image"
        path = path + "\\" + each.text()
        utils.log( "即将存放在：" + path )
        total += 1
        if total<=11:
#            continue
            pass
        else:
            param={"url":each.attr('href'),"path":path}
            craw.downimgofsite(param )


def downimgofsite(self, param):
    url = ""
    path = ""
    # path = str(path)
    if param and "url" in param:
        url = param["url"]
        utils.log("即将下载：" + url)
    else:
        utils.log("线程运行错误，url为空")
        return

    if param and "path" in param:
        path = param["path"]
        utils.log("即将保存路径：" + path)
    else:
        utils.log("线程运行错误，路径为空")
        return

    # 获取所有图集的名称和链接
    meun_list = self.getallAltls(url)
    total = 0
    directorypath = ""

    # print os.getcwd()

    try:
        for meun in meun_list:
            try:
                directoryname = self.str_fomat(meun[0])
                if not directoryname:
                    utils.log("获取到的图集为空" + str(directoryname))
                    continue
                if path.strip() != "":
                    directorypath = path + "\\" + directoryname
                else:
                    directorypath = os.getcwd() + "\\" + directoryname

                if not os.path.exists(directorypath):
                    os.makedirs(directorypath)
                    utils.log("图集 " + meun[0] + " 创建路径：" + directorypath)

                utils.log("正在下载第 " + str(total) + "个图集：" + meun[0] + " 链接：" + url)
                result = self.getSinglePic(meun[1], directorypath)
                total += 1
            except IOError, param:
                utils.log("图集：" + meun[0] + "IO读写错误，原因" + param)
                continue
            except BaseException, param:
                utils.log("图集：" + meun[0] + "产生意外错误")
                continue
            except:
                utils.log("图集：" + meun[0] + "产生意外错误，原因：" + param)
                continue

            try:
                if result:
                    utils.log("图集：" + meun[0] + " 获取链接：" + meun[1] + " 成功，共下载：" + str(result) + " 张图片")
                else:
                    os.rmdir(directorypath)
                    utils.log("图集：" + meun[0] + " 获取链接：" + meun[1] + " 失败，即将删除目录：" + directoryname)
                # self.cleanDir(directorypath)
            except WindowsError, parm:
                utils.log("操作目录：" + directoryname + "失败，原因：" + parm, logging.ERROR)
                continue
            except BaseException, parm:
                utils.log("发生错误，错误原因：" + parm, logging.ERROR)
                continue
            except:
                utils.log("发生未知错误", logging.ERROR)
                continue
    except BaseException, parm:
        utils.log("下载站点图片出错，错误原因：" + parm, logging.ERROR)