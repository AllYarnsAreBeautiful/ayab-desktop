import json
repo = {
      "kh910":
       {"mega2560":
          [
            {
              "version": "latest",
              "url": "",
              "file": "firmware.hex",
              "date": "",
              "sha1sum": ""
            },
          ],
        "uno":
          [
            {
              "version": "latest",
              "url": "/",
              "file": "firmware.hex"
            },
          ]
       },
      "kh930":
        {"mega2560":
           [
             {
               "version": "latest",
               "url": "",
               "file": "firmware.hex",
               "date": "",
               "sha1sum": ""
             },
           ],
         "uno":
           [
            {
              "version": "latest",
              "url": "/",
              "file": "firmware.hex"
            },
           ]
        },
      "hardware_test":{
        "mega2560":
          [
            {
              "version": "latest",
              "url": "/",
              "file": "firmware.hex"
            },
          ],
        "uno":
          [
            {
              "version": "latest",
              "url": "/",
              "file": "firmware.hex"
            },
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