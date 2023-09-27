import pdfplumber, json

with pdfplumber.open("Room map-jan-31-2023.pdf") as pdf:

    data = {}
    
    for page in pdf.pages:

        try:

            page_table = page.extract_table()

            if page_table == None: continue
            
            if len(page_table) != 9:
                page_table += pdf.pages[page.page_number].extract_table()
                continue

            data[f"Page {page.page_number}"] = {
                "number": page_table[0][0][8:],
                "type": page_table[1][0][5:],
                "lectureCapacity": int(page_table[1][7]),
                "examCapacity": int(page_table[1][9]),
                "fixedClasses": {
                    "monday": page_table[3][1:],
                    "tuesday": page_table[4][1:],
                    "wednesday": page_table[5][1:],
                    "thursday": page_table[6][1:],
                    "friday": page_table[7][1:],
                    "saturday": page_table[8][1:],
                }
            }
        
            print(f"[✅] Parsed page: {page.page_number}")

        except BaseException as e:
            print(f"[❌] Error parsing page: {page.page_number}\nError: {e}")
    
    try:
        with open("task.json", mode='w') as f: json.dump(data, f)
        print(f"\n[✅] Added parsed pages to JSON\n")
    except BaseException as e:
        print(f"\n[❌] Couldn't save to JSON. Error: {e}\n")