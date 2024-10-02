import argparse

import func

def main(url):
    incident_data = func.fetchincidents(url)
    
    incidents = func.extractincidents(incident_data)
    

    db = 'resources/normanpd.db'  

    func.createdb(db)
	
    func.populatedb(db, incidents)

    func.status(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
     
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
