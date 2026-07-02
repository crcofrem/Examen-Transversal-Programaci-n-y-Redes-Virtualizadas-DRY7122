asn = int(input("Ingrese el número AS: "))

if 64512 <= asn <= 65534:
    print("AS Privado")
elif 4200000000 <= asn <= 4294967294:
    print("AS Privado")
else:
    print("AS Público")
