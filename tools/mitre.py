from mitreattack.stix20 import MitreAttackData
import json
import csv

MITRE_COPYRIGHT="""
Terms of Use
LICENSE
The MITRE Corporation (MITRE) hereby grants you a non-exclusive, royalty-free license to use ATT&CK® for research, development, and commercial purposes. Any copy you make for such purposes is authorized provided that you reproduce MITRE's copyright designation and this license in any such copy.
"© 2022 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
DISCLAIMERS
MITRE does not claim ATT&CK enumerates all possibilities for the types of actions and behaviors documented as part of its adversary model and framework of techniques. Using the information contained within ATT&CK to address or cover full categories of techniques will not guarantee full defensive coverage as there may be undisclosed techniques or variations on existing techniques not documented by ATT&CK.
ALL DOCUMENTS AND THE INFORMATION CONTAINED THEREIN ARE PROVIDED ON AN "AS IS" BASIS AND THE CONTRIBUTOR, THE ORGANIZATION HE/SHE REPRESENTS OR IS SPONSORED BY (IF ANY), THE MITRE CORPORATION, ITS BOARD OF TRUSTEES, OFFICERS, AGENTS, AND EMPLOYEES, DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTY THAT THE USE OF THE INFORMATION THEREIN WILL NOT INFRINGE ANY RIGHTS OR ANY IMPLIED WARRANTIES OF MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.
"""

def main():
    mitre_attack_data = MitreAttackData("enterprise-attack.json")

    mitigations = mitre_attack_data.get_mitigations(remove_revoked_deprecated=True)

    print(f"Retrieved {len(mitigations)} ATT&CK mitigations.")
    mylib = {}
    mylib['name'] = "MITRE ATT&CK 2.1 - Mitigations"
    mylib['description'] = "Mitigations from MITRE ATT&CK 2.1"
    mylib["format_version"] = "1.0"
    mylib["copyright"] = MITRE_COPYRIGHT
    mylib["locale"] = "en"
    mylib["objects"] = []
    for m in mitigations:
        name = m.name
        id = m.external_references[0].external_id
        url = m.external_references[0].url
        description = m.description.strip(" \n")
        print(id, name)
        secfunc = {"type": "security_function", "fields": {
            "name": f"{id} - {name}", 
            "description": description + "\n" + url + "\n", 
            "provider": "MITRE ATT&CK"}}
        mylib["objects"].append(secfunc)
    with open("mitre-mitigations.json", "w") as f:
        json.dump(mylib, f, indent=2)
    with open('measures.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for m in mitigations:
            writer.writerow([m.external_references[0].external_id, m.name, m.description.strip(" \n"), m.external_references[0].url])
    with open('measures_fr.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        mylib['name'] = "MITRE ATT&CK 2.1 - Fonctions de sécurité"
        mylib['description'] = "Fonctions de sécurité depuis MITRE ATT&CK 2.1"
        mylib["locale"] = "fr"
        mylib["objects"] = []
        for (id, name, description, url) in reader:
            print(id, name)
            secfunc = {"type": "security_function", "fields": {
                "name": f"{id} - {name}", 
                "description": description + "\n" + url + "\n", 
                "provider": "MITRE ATT&CK"}}
            mylib["objects"].append(secfunc)
        with open("mitre-mitigations-fr.json", "w") as f:
            json.dump(mylib, f, indent=2)


    techniques = mitre_attack_data.get_techniques(remove_revoked_deprecated=True)

    print(f"Retrieved {len(techniques)} ATT&CK techniques.")
    mylib = {}
    mylib['name'] = "MITRE ATT&CK 2.1 - Techniques"
    mylib['description'] = "Main techniques from MITRE ATT&CK 2.1"
    mylib["format_version"] = "1.0"
    mylib["copyright"] = MITRE_COPYRIGHT
    mylib["objects"] = []
    main_techniques = [t for t in techniques if not t.x_mitre_is_subtechnique]
    print(len(main_techniques))
    for t in main_techniques:
        name = t.name
        id = t.external_references[0].external_id
        url = t.external_references[0].url
        description = t.description.strip(" \n")
        print(id, name)
        threat = {"type": "threat", "fields": {
            "name": f"{id} - {name}", 
            "description": description + "\n" + url + "\n",
            "provider": "MITRE ATT&CK"}}
        mylib["objects"].append(threat)
    with open("mitre-techniques.json", "w") as f:
        json.dump(mylib, f, indent=2)
    with open('techniques.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for t in main_techniques:
            writer.writerow([t.external_references[0].external_id, t.name, t.description.strip(" \n"), t.external_references[0].url])
    with open('techniques_fr.csv', 'r', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        mylib['name'] = "MITRE ATT&CK 2.1 - Menaces"
        mylib['description'] = "Menaces depuis MITRE ATT&CK 2.1"
        mylib["locale"] = "fr"
        mylib["objects"] = []
        for (id, name, description, url) in reader:
            print(id, name)
            secfunc = {"type": "threat", "fields": {
                "name": f"{id} - {name}", 
                "description": description + "\n" + url + "\n", 
                "provider": "MITRE ATT&CK"}}
            mylib["objects"].append(secfunc)
        with open("mitre-techniques-fr.json", "w") as f:
            json.dump(mylib, f, indent=2)


if __name__ == "__main__":
    main()
