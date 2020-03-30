# coding=utf-8
import xlrd
import argparse
import myLibrary as myLib
import os.path
import shutil

parser = argparse.ArgumentParser(description='İSA GİRİŞKEN')
parser.add_argument('--verimodeli', type=str,
                    help='Tablo yapısını wordten kopyala excele yapıştır yolu buraya ver')
parser.add_argument('--tabloAdi', type=str,
                    help='wordteki tablo adi')
parser.add_argument('--serverpath', type=str,
                    help='client-server arasındaki path')
parser.add_argument('--filterexcel', type=str,
                    help="Filtre Listesinin formunu excele kopyala yolunu ver")
parser.add_argument('--alanlistesi', type=str,
                    help="Liste ekranının alan listesini excele kopyala yolunu ver.")
parser.add_argument('--tanimlistesi', type=str
                    , help="Kayıt ekranı wordteki dosyasını excele kopyala yolunu ver.")
parser.add_argument('--kayityeri', type=str, help="dosya ciktilarinin kayit edileceği yer.")
parser.add_argument("--dosyaadi", type=str, help="kayıt edilecek dosya adı..")

args = parser.parse_args()

wb = xlrd.open_workbook(args.verimodeli)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)


# #ENTİTY İÇİN

def entityAndTs():
    model = open("models/entityModel.txt", "rt", encoding="utf8")
    model2 = open("models/frontModel.txt", "rt", encoding="utf8")
    temp = open("entityEklenecek.txt", "a+", encoding="utf8")
    temp2 = open("tsEklenecek.txt", "a+", encoding="utf8")
    wb = xlrd.open_workbook(args.verimodeli)
    sheet = wb.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        cell = sheet.cell_value(i, 0)
        type = sheet.cell_value(i, 1)
        meta = sheet.cell_value(i, 3)
        type.replace(" ", "")
        temp.write('@Column(name=' + '\"' + cell + '\")' + '\n')
        temp.write('private ' + myLib.entityType(str(type), str(meta)) + ' ' + myLib.camelCase(cell) + ';\n')
        temp2.write(myLib.camelCase(cell) + ':' + myLib.angularType(type) + ';\n')
    temp.close()
    temp2.close()
    temp = open("entityEklenecek.txt", "rt", encoding="utf8")
    temp2 = open("tsEklenecek.txt", "rt", encoding="utf8")
    entityReady = open("entityReady.txt", "w+", encoding="utf8")
    fronModelReady = open("frontModelReady.txt", "w+", encoding="utf8")
    myLib.checkWords = ("eklenecek", "className", "tableName")
    myLib.repWords = (temp.read(), myLib.className(args.tabloAdi), args.tabloAdi)
    myLib.changeLines(model, entityReady)
    myLib.repWords = (temp2.read(), myLib.className(args.tabloAdi), args.tabloAdi)
    myLib.changeLines(model2, fronModelReady)
    fronModelReady.close()
    entityReady.close()
    temp.close()
    temp2.close()
    os.remove("entityEklenecek.txt")
    os.remove("tsEklenecek.txt")
    model.close()
    model2.close()


def changeLog():
    model = open("models/changelog.txt", "rt", encoding="utf8")
    temp1 = open("changelogEklenecek.txt", "a+", encoding="utf8")
    ab = xlrd.open_workbook(args.verimodeli)
    sheet = ab.sheet_by_index(0)
    for i in range(2, sheet.nrows):
        cell = sheet.cell_value(i, 0)
        type = sheet.cell_value(i, 1)
        type.replace(" ", "")
        temp1.write('<column name=\"' + cell + '\"  type=\"' + type + '\" />' + '\n')
    temp1.close()
    temp = open("changelogEklenecek.txt", "rt", encoding="utf8")
    changeReady = open("changelogReady.txt", "w+", encoding="utf8")
    myLib.checkWords = ("tableName1", "tableName2", "eklenecek")
    myLib.repWords = (args.tabloAdi, str(args.tabloAdi).replace("_", ""), temp.read())
    myLib.changeLines(model, changeReady)
    temp.close()
    changeReady.close()
    os.remove("changelogEklenecek.txt")


# ANGULAR SERVİCE
def frontService():
    s = open("models/serviceModel.txt", "rt")
    s1 = open("frontService.txt", "w+")
    myLib.checkWords = ("className", "objectName", "serverPath")
    myLib.repWords = (myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi), args.serverpath)
    myLib.changeLines(s, s1)
    s.close()
    s1.close()


parametre = open("parametre.txt", "a+", encoding="utf8")


# ANGULAR COMPONENT LİST
def componentList():
    model = open("models/componentList.txt", "rt", encoding='utf8')
    target = open("componentListReady.txt", "w+", encoding='utf8')
    filter = open("filtreEklenecek.txt", "a+", encoding="utf8")
    wb = xlrd.open_workbook(args.filterexcel)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1, sheet.nrows):
        baslik = sheet.cell_value(i, 0)
        veri = sheet.cell_value(i, 1)
        tip = sheet.cell_value(i, 2)
        label = myLib.changeTr(myLib.camelCase(baslik.replace(" ", "_")))
        if "date" in tip.lower():
            parametre.write("@Param(" + "\"kontrol" + label.capitalize() + "\" ) boolean kontrol" + label.capitalize() + ", \n")
            parametre.write("@Param(\"" + label + "Baslangic\") Date " + label + "Baslangic, \n")
            parametre.write("@Param(\"" + label + "Bitis\") Date " + label + "Bitis, \n")
        else:
            parametre.write("@Param(\"" + label + "\")" + myLib.daoParam(tip) + " " + label + ", \n")
        try:
            if "date" in tip.lower():
                filter.write(label + 'Baslangic:null,' + '\n')
                filter.write(label + 'Bitis:null,' + '\n')
            else:
                filter.write(label + ':null,' + '\n')
        except IndexError:
            print (
                        "Filtreler.xlsx--- " + "\'" + veri + "\'" + " --Alanında Veri Okuma Hatası.Düzeltip Tekrar Deneyiniz.")
    parametre.close()
    filter.close()
    temp1 = open("filtreEklenecek.txt", "rt", encoding="utf8")
    wb = xlrd.open_workbook(args.alanlistesi)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    #######
    export = open("newArray.txt", "a+", encoding="utf8")
    headers = open("headers.txt", "a+", encoding="utf8")
    for i in range(1, sheet.nrows):
        baslik = sheet.cell_value(i, 0)
        if ("tarih" in str(baslik).lower()):
            export.write(baslik.replace(" ", "_") + ": this.help.dateTransform(o." + myLib.changeTr(
                myLib.camelCase(baslik)) + '),' + '\n')
        else:
            export.write(baslik.replace(" ", "_") + ":o." + myLib.changeTr(myLib.camelCase(baslik)) + ',' + '\n')
        if i % 5 == 0:
            headers.write("\"" + baslik + "\"," + '\n')
        else:
            headers.write("\"" + baslik + "\",")
    export.close()
    headers.close()
    export1 = open("newArray.txt", "r+", encoding="utf8")
    header1 = open("headers.txt", "r+", encoding="utf8")
    myLib.checkWords = ("className", "objectName", "serverPath", "filtreEklenecek", "basliklar", "exportList")
    myLib.repWords = (
    myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi), args.serverpath, temp1.read(), header1.read(),
    export1.read())
    myLib.changeLines(model, target)
    model.close()
    target.close()
    temp1.close()
    export1.close()
    header1.close()
    os.remove("headers.txt")
    os.remove("newArray.txt")
    os.remove("filtreEklenecek.txt")


# ANGULAR COMPONENT EDİT
def componentEdit():
    mdl = open("models/componentEdit.txt", "rt", encoding="utf8")
    trgt = open("componentEditReady.txt", "w+", encoding="utf8")
    myLib.checkWords = ("className", "objectName", "serverPath")
    myLib.repWords = (myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi), args.serverpath)
    myLib.changeLines(mdl, trgt)
    mdl.close()
    trgt.close()

asFile = open("asSorgusu.txt","a+",encoding="utf8")
# HTML LİSTFİLTER KISMI
def htmlList():
    wb = xlrd.open_workbook(args.filterexcel)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1, sheet.nrows):
        label = sheet.cell_value(i, 0)
        veri = sheet.cell_value(i, 1)
        tipi = sheet.cell_value(i, 2)
        meta = sheet.cell_value(i, 4)

        comboParameter = "null"
        if ("code" in meta):
            comboParameter = str(meta).split(':').pop()
            comboParameter = comboParameter[0].upper() + comboParameter[1:]
        myLib.checkWords = ("labelName", "objectName", "className", "tableName1", "serverPath", "parametre")
        try:
            myLib.repWords = (label, myLib.changeTr(myLib.camelCase(label.replace(" ", "_"))),
                              myLib.className(str(veri).split('.').pop()), str(meta).split('.').pop(0), args.serverpath,
                              comboParameter)
        except IndexError:
            print(
                        args.filterexcel + " " + "Dosyasında " + " " + veri + " - " + meta + " Alanında İmla Hatası Düzeltip Tekrar Deneyiniz.")
        myLib.htmlFilterList(label, str(tipi).lower(), meta)


# HTML LİSTALAN KISMIe
def htmlAlanListesi():
    wb = xlrd.open_workbook(args.alanlistesi)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1, sheet.nrows):
        label = sheet.cell_value(i, 0)
        veri = sheet.cell_value(i, 1)
        tipi = sheet.cell_value(i, 2)
        meta = sheet.cell_value(i, 3)
        myLib.htmlAlanList(label, tipi, myLib.changeTr(myLib.camelCase(label.replace(" ", "_"))), meta)
        try:
            asFile.write(" \"p." + myLib.camelCase(veri.split(".").pop(1)) + " as " + myLib.changeTr(myLib.camelCase(label.replace(" ", "_"))) + " , \" + \n")
        except IndexError:
            print("Alan Listesi Excel Dosyasında " + label + " " + veri + " Alanında İmla Hatası Kontrol Ediniz.")
    asFile.close()


def htmlEdit():
    wb = xlrd.open_workbook(args.tanimlistesi)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1, sheet.nrows):
        label = sheet.cell_value(i, 0)
        veri = sheet.cell_value(i, 1)
        tipi = sheet.cell_value(i, 2)
        meta = sheet.cell_value(i, 3)
        camelVeri = myLib.camelCase(str(veri).split('.').pop())
        classVeri = myLib.className(str(veri).split('.').pop())
        comboParameter = "BULUNAMADI"
        if ("code" in meta.lower()):
            comboParameter = str(meta).split(':').pop(1)
            comboParameter = comboParameter[0].upper() + comboParameter[1:]
        if "enum" in meta.lower():
            comboParameter = str(meta).split(':').pop(1)
            comboParameter = comboParameter[0].upper() + comboParameter[1:]
        myLib.checkWords = (
        "labelName", "tableName1", "className", "camelTable", "objectName", "tableIndex", "parametre")
        myLib.repWords = (label, str(meta).split('.').pop(0), classVeri, myLib.camelCase(args.tabloAdi), camelVeri,
                          str(meta).split('.').pop(), comboParameter)
        myLib.htmlEditListInputs(label, veri, str(tipi).lower(), meta, args.tabloAdi)


def htmlBirlestir():
    htmlModel = open("models/htmlListModel.txt", "rt", encoding="utf8")
    htmlListReady = open("htmlListReady.txt", "w+", encoding="utf8")
    htmlTemplateFilter = open("htmlTemplate.txt", "rt", encoding="utf8")
    htmlAlanLabel = open("htmlAlanEklenecekLabel.txt", "rt", encoding="utf8")
    htmlAlanList = open("htmlAlanEklenecekList.txt", "rt", encoding="utf8")
    myLib.checkWords = ("eklenecek1", "className", "objectName", "labelEklenecek", "alaneklenecek", "serverPath")
    myLib.repWords = (str(htmlTemplateFilter.read()), myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi),
                      str(htmlAlanLabel.read()), str(htmlAlanList.read()), args.serverpath)
    myLib.changeLines(htmlModel, htmlListReady);
    htmlEditReady = open("htmlEditReady.txt", "w+", encoding="utf8")
    htmlTemplateEdit = open("htmlEditEklenecek.txt", "rt", encoding="utf8")
    htmlEditModel = open("models/editHtmlModel.txt", "rt", encoding="utf8")
    myLib.checkWords = ("eklenecek", "className", "objectName", "serverPath")
    myLib.repWords = (
    str(htmlTemplateEdit.read()), myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi), args.serverpath)
    myLib.changeLines(htmlEditModel, htmlEditReady);
    # delete = open("htmlTemplate.txt", "w+")
    # delete2 = open("htmlAlanEklenecekLabel.txt","w+")
    # delete3 = open("htmlAlanEklenecekList.txt", "w+")
    # delete = open("htmlEditEklenecek.txt","w+")


def dao():
    model = open("models/BackDao.txt", "rt", encoding="utf8")
    temp = open("daoEklenecek.txt", "w+", encoding="utf8")
    parametreler = open("parametre.txt", "rt", encoding="utf8")
    asFile1 = open("asSorgusu.txt","rt",encoding="utf8")
    myLib.checkWords = ("className", "parametreler","sorgu")
    myLib.repWords = (myLib.className(args.tabloAdi), parametreler.read(),asFile1.read())
    myLib.changeLines(model, temp)
    model.close()
    temp.close()
    parametreler.close()
    asFile1.close()
    os.remove("parametre.txt")
    os.remove("asSorgusu.txt")


# BACKEND CONTROLLER
def backController():
    x = open("models/backControllerModel.txt", "rt", encoding="utf8")
    y = open("BackController.txt", "w+", encoding="utf8")
    filtre = open("filtreEklenecek.txt", "a+", encoding="utf8")
    wb = xlrd.open_workbook(args.filterexcel)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    for i in range(1, sheet.nrows):
        label = sheet.cell_value(i,0)
        veri = sheet.cell_value(i, 1)
        type = sheet.cell_value(i, 2)
        meta = sheet.cell_value(i, 4)
        baslik = myLib.changeTr(myLib.camelCase(label.replace(" ","_")))
        if "date" in type.lower():
            filtre.write(
                "filter.shouldFilterRange(" + "\"" + baslik + "Baslangic" + "\"" + ",\"" + baslik + "Bitis" + "\") , \n" )
            filtre.write(
                "filter.getDateOrMin(" + "\"" + baslik + "Baslangic" + "\"),\n")
            filtre.write(
                "filter.getDateOrMax(" + "\"" + baslik + "Bitis")
        else:
            filtre.write(
                "filter.get" + myLib.filterType(str(type).lower(), str(meta).lower()) + "(\"" + myLib.camelCase(
                    str(veri).split(".").pop()))

        filtre.write("\"" + "),")
        filtre.write("\n")
    filtre.close()
    filtre = open("filtreEklenecek.txt", "rt", encoding="utf8")
    myLib.checkWords = ("className", "objectName", "serverpath", "filtreEklenecek")
    myLib.repWords = (myLib.className(args.tabloAdi), myLib.camelCase(args.tabloAdi), args.serverpath, filtre.read())
    myLib.changeLines(x, y)
    x.close()
    y.close()
    filtre.close()
    os.remove("filtreEklenecek.txt")


def save():
    dir = os.path.join(str(args.kayityeri), str(args.dosyaadi))
    os.mkdir(dir)
    javadir = os.path.join(dir, "BackEnd")
    os.mkdir(javadir)
    angulardir = os.path.join(dir, "FrontEnd")
    os.mkdir(angulardir)
    shutil.move("entityReady.txt", str(javadir))
    shutil.move("componentEditReady.txt", str(angulardir))
    shutil.move("componentListReady.txt", str(angulardir))
    shutil.move("frontModelReady.txt", str(angulardir))
    shutil.move("frontService.txt", str(angulardir))
    shutil.move("htmlEditReady.txt", str(angulardir))
    shutil.move("htmlListReady.txt", str(angulardir))
    shutil.move("BackController.txt", str(javadir))
    shutil.move("daoEklenecek.txt", str(javadir))
    shutil.move("changelogReady.txt", str(javadir))
    os.rename(os.path.join(angulardir, "componentEditReady.txt"),
              os.path.join(angulardir, str(args.tabloAdi).lower().replace("_", "-") + "-edit.component.ts"))
    os.rename(os.path.join(angulardir, "componentListReady.txt"),
              os.path.join(angulardir, str(args.tabloAdi).lower().replace("_", "-") + "-list.component.ts"))
    os.rename(os.path.join(angulardir, "frontModelReady.txt"),
              os.path.join(angulardir, myLib.className(str(args.tabloAdi)) + ".ts"))
    os.rename(os.path.join(angulardir, "frontService.txt"),
              os.path.join(angulardir, myLib.className(str(args.tabloAdi)) + "Service.ts"))
    os.rename(os.path.join(angulardir, "htmlEditReady.txt"),
              os.path.join(angulardir, str(args.tabloAdi).lower().replace("_", "-") + "-edit.component.html"))
    os.rename(os.path.join(angulardir, "htmlListReady.txt"),
              os.path.join(angulardir, str(args.tabloAdi).lower().replace("_", "-") + "-list.component.html"))
    os.rename(os.path.join(javadir, "BackController.txt"),
              os.path.join(javadir, myLib.className(str(args.tabloAdi)) + "Controller.java"))
    os.rename(os.path.join(javadir, "entityReady.txt"), os.path.join(javadir, myLib.className(args.tabloAdi) + ".java"))
    os.rename(os.path.join(javadir, "daoEklenecek.txt"),
              os.path.join(javadir, myLib.className(args.tabloAdi) + "Dao.java"))
    os.rename(os.path.join(javadir, "changelogReady.txt"),
              os.path.join(javadir, myLib.className(args.tabloAdi) + "changelog.xml"))
    os.remove("htmlAlanEklenecekLabel.txt")
    os.remove("htmlAlanEklenecekList.txt")
    os.remove("htmlEditEklenecek.txt")
    os.remove("htmlEklenecek.txt")
    os.remove("htmlTemp.txt")
    os.remove("htmlTemplate.txt")


backController()
entityAndTs()
changeLog()
frontService()
componentList()
componentEdit()
htmlList()
htmlAlanListesi()
htmlEdit()
htmlBirlestir()
dao()
save()
