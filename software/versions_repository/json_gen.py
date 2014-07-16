import json
repo = {
      "kh910":
       {"mega2560":
          [
            {"version": "latest",
             "url": "/",
             "date": "",
             "sha1sum": ""
            },
            {"version": "v3",
             "url":"/kh910/mega2560/ayab_kh910_mega_v3.hex"},
          ],
        "uno":
          [
            {"version": "latest",
             "url": "/"},
            {"version":"v3",
             "url": "/kh910/uno/ayab_k910_uno_v3.hex"},
          ]
       },
      "kh930":
        {"mega2560":
           [
             {"version": "latest",
              "url": "/kh930/mega/ayab_kh930_mega_v3.hex"}
           ],
         "uno":
           [
              {"version": "latest",
               "url": "/kh930/uno/ayab_kh930_uno_v3.hex"}
           ]
        },
      "hardware_test":{
        "mega2560":
          [
            {"version":"latest",
             "date": "",
             "sha1sum": ""},
          ],
        "uno":
          [
            {"version": "latest"}
          ]
        }
     }
print("==")
repo_string = json.dumps(repo)
with open('example_repo.json', 'wb') as configfile:
  configfile.write(repo_string)
print(repo_string)
print("==")
for hardware_device in repo:
  print(hardware_device)
  for controller in repo[hardware_device]:
    print controller
    for firmware in repo[hardware_device][controller]:
      print firmware["version"]