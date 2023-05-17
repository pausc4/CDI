import sys

filename = sys.argv[1]
txt = open(filename).read()

txt = txt.lower()
txt = txt.replace("à", "a"); txt = txt.replace("á", "a"); txt = txt.replace("â", "a"); txt = txt.replace("ä", "a")
txt = txt.replace("è", "e"); txt = txt.replace("é", "e"); txt = txt.replace("ê", "e"); txt = txt.replace("ë", "e")
txt = txt.replace("ì", "i"); txt = txt.replace("í", "i"); txt = txt.replace("î", "i"); txt = txt.replace("ï", "i")
txt = txt.replace("ò", "o"); txt = txt.replace("ó", "o"); txt = txt.replace("ô", "o"); txt = txt.replace("ö", "o")
txt = txt.replace("ù", "u"); txt = txt.replace("ú", "u"); txt = txt.replace("û", "u"); txt = txt.replace("ü", "u")
txt = txt.replace("ç", "c"); txt = txt.replace("ß", "ss"); txt = txt.replace("ñ", "n")
txt = txt.replace("·", ""); txt = txt.replace(".", ""); txt = txt.replace("º", ""); txt = txt.replace("ª", "");
txt = txt.replace(",", ""); txt = txt.replace(":", ""); txt = txt.replace("?", ""); txt = txt.replace(";", "");
txt = txt.replace("", ""); txt = txt.replace("-", " "); txt = txt.replace("'", " "); txt = txt.replace("\n", " ");
txt = txt.replace("_", " "); txt = txt.replace("*", ""); txt = txt.replace("«", " "); txt = txt.replace("»", " "); 
txt = txt.replace("\ufeff", " "); txt = txt.replace("(", " "); txt = txt.replace(")", " "); txt = txt.replace("¡", " ");
txt = txt.replace("!", " "); txt = txt.replace("¿", " "); txt = txt.replace("\"", " "); txt = txt.replace("]", " ")
txt = txt.replace("[", " ")
txt = txt.replace("  ", " "); txt = txt.replace("  ", " ");

open(filename[:-4] + "_clean.txt", "w").write(txt)