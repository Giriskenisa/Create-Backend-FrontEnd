@echo off

set /p table_name="Table Name = "
set /p server_path="Server Path = "
set /p dosya_adi="Dosya Adi = "



python main.py --verimodeli verimodeli.xlsx --tabloAdi %table_name% --serverpath %server_path% --filterexcel filtreler.xlsx --alanlistesi alanlistesi.xlsx --tanimlistesi tanimlistesi.xlsx --kayityeri C:\Users\Girisken\Desktop --dosyaadi %dosya_adi%

@echo.
@echo.
@pause