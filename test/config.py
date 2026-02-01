
MOCK_CSV = """user_id,manager_id,name,email_address,start_date,last_login
EFEABEA5-981B-4E45-8F13-425C456BF7F6,CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,Ashley Hernandez,ashley.hernandez@live.com,2025-Mar-01,2025-03-23 16:54:43 CET
2AB96C22-181C-42DC-8B11-3EDAA281D4F8,A37D98B9-98E7-43ED-9B27-A79EFDDAC033,Lisa Nelson,lisa.nelson@outlook.com,2021-Feb-17,2025-02-27 16:35:22 CET
0213F1C0-01D9-422C-8737-19FBFA902082,4828D9F6-5959-4646-92AD-8A8AD49ABE4A,Amanda Roberts,amanda.roberts@live.com,2020-Jun-19,2025-03-07 17:29:50 CET
4828D9F6-5959-4646-92AD-8A8AD49ABE4A,A37D98B9-98E7-43ED-9B27-A79EFDDAC033,Jennifer Rodriguez,jennifer.rodriguez@protonmail.com,2021-Oct-01,2025-02-14 03:48:32 CET
850A74DC-8ED7-4AE0-A998-94A30E8C1E4C,CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,Melissa Jackson,melissa.jackson@acme.co,2024-Mar-21,2025-01-22 06:46:54 CET
CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,880036D9-568A-47BC-80FB-3C9BC5D74313,Dorothy Parker,dorothy.parker@acme.co,2021-Aug-01,2025-03-02 20:19:49 CET
880036D9-568A-47BC-80FB-3C9BC5D74313,CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,Sandra Johnson,sandra.johnson@msn.com,2021-Sep-02,2025-01-19 11:14:18 CET
78FFE618-36C0-4A45-BB0F-8803B79D2A1F,CDD3AA5D-F8BF-40BB-B220-36147E1B75F7,Ronald Hall,ronald.hall@mail.com,2024-Mar-02,2025-04-07 07:14:09 CET
6A6EE61B-2793-4D65-BDC5-14F849AEEC32,0213F1C0-01D9-422C-8737-19FBFA902082,Daniel Turner,daniel.turner@live.com,2023-Nov-19,2025-04-02 14:11:20 CET
"""


SAMPLE_DATA = []
for line in MOCK_CSV.strip().splitlines()[1:]:
        cols = line.split(",")
        SAMPLE_DATA.append({
            "user_id": cols[0],
            "manager_id": cols[1],
            "name": cols[2],
            "email_address": cols[3],
            "start_date": cols[4],
            "last_login": cols[5],
        })

