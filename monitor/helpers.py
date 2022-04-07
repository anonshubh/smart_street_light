import requests

write_key = "Q8JBF7C1RKKAXK50"

def send_data_to_thingSpeak(data):
    URL = f"https://api.thingspeak.com/update?api_key={write_key}"

    params={
        'field1':data['temperature'],
        'field2':data["humidity"],
        'field3':data["ir"],
        'field4':data["light"],
    }
    
    requests.get(URL,params=params)


def take_action(data):
    light = int(data['light'])
    ir = int(data['ir'])
    result = {}
    if(light < 600):
        result['status'] = 1 # ON
    else:
        result['status'] = 0 # OFF
    
    result['intensity'] = 30*ir

    return result