import xnat
import toml


def PatientQuery(config, **kwargs):
    config = toml.load('../SettingsCAE.ini')
    session = xnat.connect('http://128.16.11.124:8080/xnat/', user='yzhan', password='yzhan')
    sandbox_project = session.projects["RTOG_test"]
    subjects = sandbox_project.subjects.filter(label='0617-*')
    for subject in subjects.values():
        # image, dose, plan, structure scans
        scan_data = subject.experiments[subject.label].scans
        clinical_data = subject.fields.keys()

    for key, items in config['CRITERIA'].items():
        for item in items:
            subject = subjects.get('0617-' + item)
            if subject:
            subjects.listing.remove(subject)

    return sandbox_project.subjects
