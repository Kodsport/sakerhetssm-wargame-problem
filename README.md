# wargame-problem
To add new challenges to the wargame, the challenge.yml of each chall need to be modified. To find vacant ports, run `python3 ./utils/find_vacant_port.py`, port range should be 40000-50000.
```yml
service:
  type: website
  image: container
  internal_port: 1337
  external_port: 44444 # Make sure to add external_port (use ./utils/find_vacant_port.py to find a vacant port)

# website service
predefined_services:
- type: website
  url: http://188.126.67.132:44444 # Change this port to the external_port

# tcp service
predefined_services:
  - type: tcp
    host: 188.126.67.132
    port: 44444 # Change this port to the external_port

human_metadata:
  event_name: SSM 2024 Kval # This should be the event-name as its displayed on https://sakerhetssm.se/challenges

score: 450 # Don't forget to add score

custom:
  publish: true # If the challenge should be published on https://sakerhetssm.se/challenges
```