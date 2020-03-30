# coding=utf-8
def entityType(st, meta):
    if ("NUMBER" in st):
        if ("(1)" in st):
            return "Boolean"
        elif ("38" in st):
            return "Long"
        elif ("19" in st):
            return "Long"
        else:
            return "Integer"
    elif ("VARCHAR" in st):
        if ("bool" in meta):
            return "Boolean"
        else:
            return "String"
    elif ("DATE" in st or "STAMP" in st):
        return "Date"
    elif ("clob" in st.lower()):
        return "String"
    else:
        return "BULUNAMADI"


def filterType(st, meta):
    if ("number" in st):
        if ("(38)" or "(19)" in st):
            return "Long"
        elif ("(1)" in st):
            return "Boolean"
        else:
            return "Integer"
    elif ("varchar" in st or "text" in st):
        return "String"
    elif ("date" in st or "timestamp" in st):
        return "DateOrMin"
    elif ("ajax" in st):
        return "Long"
    elif ("box" in st):
        if ("bool" in meta):
            return "Boolean"
        else:
            return "String"
    else:
        return "BULUNAMADI"

def daoParameter(type):
    type1 = type.lower()
    if "ajax" in type1:
        return "Long"
    if "date" in type1:
        return "Date"
    return "String"


def angularType(st):
    if ("NUMBER" in st):
        if ("(1)" in st):
            return "boolean=false";
        else:
            return "Number"
    elif ("VARCHAR" in st):
        if "(1)" in st:
            return "boolean=false";
        else:
            return "String";
    elif ("DATE" or "TIME" in st):
        return "Date"
    else:
        return "BULUNAMADI"


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


def className(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].upper() + output[1:]


checkWords = ()
repWords = ()


def changeLines(s, s1):
    for line in s:
        for check, rep in zip(checkWords, repWords):
            line = line.replace(check, rep)
        s1.write(line)


def htmlFilterList(label, tip, meta):
    if ("combobox" in tip):
        if ("code" in meta):
            model = open("models/ComboBoxFilterParameter.txt", "rt", encoding="utf8")
            target = open("htmlEklenecek.txt", "w+", encoding="utf8")
            changeLines(model, target)
        else:
            model = open("models/comboBoxModel.txt", "rt", encoding="utf8")
            target = open("htmlEklenecek.txt", "w+", encoding="utf8")
            changeLines(model, target)

    elif ("text" in tip):
        model = open("models/textModel.txt", "rt", encoding="utf8")
        target = open("htmlEklenecek.txt", "w+", encoding="utf8")
        changeLines(model, target)
    elif ("ajax" in tip):
        model = open("models/ajaxModel.txt", "rt", encoding="utf8")
        target = open("htmlEklenecek.txt", "w+", encoding="utf8")
        changeLines(model, target)
    elif ("date" in tip):
        model = open("models/dateModel.txt", "rt", encoding="utf8")
        target = open("htmlEklenecek.txt", "w+", encoding="utf8")
        changeLines(model, target)
    else:
        print("BULUNAMADI")
        return
    with open("htmlTemplate.txt", "a+", encoding="utf8") as myfile:
        target.seek(0)
        myfile.write("\n <br> \n" + str(target.read()))


def htmlAlanList(label, tip, veri, meta):
    target = open("htmlAlanEklenecekLabel.txt", "a+", encoding="utf8")
    target.write("<th scope=col>" + label + "</th>\n")
    liste = open("htmlAlanEklenecekList.txt", "a+", encoding="utf8")
    if ("combo" in tip.lower()):
        if ("@code" in meta.lower()):
            liste.write(
                "  <td *ngIf=\"dto.parametrelistesiAdi; else void\">{{dto." + veri + "}}</td>")
        else:
            liste.write(
                "<td *ngIf=\"dto." + veri + "\"><i style=\"margin-left: 30%;\" class=\"material-icons\">done</i></td>\n")
    elif ("Text" in tip):
        liste.write("<td>{{dto." + veri + "}}</td>\n")
    elif ("Date" in tip):
        liste.write("<td>{{dto." + veri + " | date:'dd-MM-yyyy'}}</td>\n")
    else:
        liste.write("<td>{{dto." + veri + "}}</td>\n")


def helper(model1):
    target = open("htmlEditEklenecek.txt", "a+", encoding="utf")
    model1.seek(0)
    target.write(str(model1.read()) + '\n' + '<br>' + '\n')


def htmlEditListInputs(label, veri, tip, meta, tableName):
    if ("ajax" in tip or "eşit" in tip):
        model = open("models/editHtmlAjaxModel.txt", "rt", encoding="utf8")
        model1 = open("htmlTemp.txt", "w+", encoding="utf8")
        changeLines(model, model1)
        helper(model1)
    elif "check" in tip:
        model = open("models/editHtmlCheckModel.txt", "rt", encoding="utf8")
        model1 = open("htmlTemp.txt", "w+", encoding="utf8")
        changeLines(model, model1)
        helper(model1)
    elif "text" in tip:
        if "area" in tip:
            model = open("models/editHtmlTextareaModel.txt", "rt", encoding="utf8")
            model1 = open("htmlTemp.txt", "w+", encoding="utf8")
            changeLines(model, model1)
            helper(model1)
        else:
            model = open("models/editHtmlTextModel.txt", "rt", encoding="utf8")
            model1 = open("htmlTemp.txt", "w+", encoding="utf8")
            changeLines(model, model1)
            helper(model1)
    elif ("combo" in tip or "tekli" in tip):
        model = open("models/editHtmlComboboxModel.txt", "rt", encoding="utf8")
        model1 = open("htmlTemp.txt", "w+", encoding="utf8")
        changeLines(model, model1)
        helper(model1)
    elif "date" in tip:
        model = open("models/editHtmlDateModel.txt", "rt", encoding="utf8")
        model1 = open("htmlTemp.txt", "w+", encoding="utf8")
        changeLines(model, model1)
        helper(model1)
    elif "number" in tip:
        model = open("models/editHtmlNumberModel.txt", "rt", encoding="utf8")
        model1 = open("htmlTemp.txt", "w+", encoding="utf8")
        changeLines(model, model1)
        helper(model1)
    else:
        print("HATALI VERİ GİRİŞİ", label, ' ', veri, ' ', tip, ' ', meta)


def changeTr(str):
    tr = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
    eng = ['c', 'g', 'i', 'o', 's', 'u', 'C', 'G', 'I', 'O', 'S', 'U']
    for i in range(0, 11):
        if tr[i] in str:
            str = str.replace(tr[i], eng[i])
    return str


def daoParam(type):
    type1 = type.lower()
    if "ajax" in type1:
        return "Long"
    elif "date" in type1:
        return "Date"
    else:
        return "String"


