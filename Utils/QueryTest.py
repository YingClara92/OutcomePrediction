import xnat
import toml

# def PatientQuery(config, **kwargs):
config = toml.load('../SettingsCAE.ini')
session = xnat.connect('http://128.16.11.124:8080/xnat/', user='yzhan', password='yzhan')
sandbox_project = session.projects["RTOG_test"]
subjects = sandbox_project.subjects.filter(label='0617-*')


def key_convert(r_key):
    if r_key in 'CTs from rtog conversion':
        r_key = 'CTs from rtog conversion'
    if r_key in 'RTStruct from rtog conversion':
        r_key = 'RTStruct from rtog conversion'
    if r_key in 'RT Plan (excerpt) - fx1hetero':
        r_key = 'RT Plan (excerpt) - fx1hetero'
    if r_key in 'RT Dose - fx1hetero':
        r_key = 'RT Dose - fx1hetero'
    return r_key


for subject in subjects.values():
    # image, dose, plan, structure scans
    scan_data = subject.experiments[subject.label].scans
    clinical_data = subject.fields
    for key, items in config['CRITERIA'].items():
        if 'images' == key:
            required_keys = config['CRITERIA']['images']
            for r_key in required_keys:
                r_key = key_convert(r_key)
                if not (r_key in scan_data.keys()):
                    subjects.listing.remove(subject)
                    break
        if key in clinical_data.keys():
            if not (clinical_data[key] in items):
                subjects.listing.remove(subject)
                break

print('subject:', subjects.listing)


# for key, items in config['CRITERIA'].items():
#     for item in items:
#         subject = subjects.get('0617-' + item)
#         if subject:
#             subjects.listing.remove(subject)

# return sandbox_project.subjects
