#!/usr/bin/env python
#use at own risk
#clears old user posts from rocket chat past 30 days and removes uploaded files as well to conserve disk space
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import datetime
import subprocess
import re

def main():
    #This grabs the current date but 30 days back
    start_date = str(datetime.datetime.now() + datetime.timedelta(-30))[:10]
    #This removes any messages 30+ days old
    subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_message.remove( { ts: { $lt: ISODate(\""""+start_date+"""\") } } );'""", shell=True)
    #This grabs any uploaded files that are 30+ days old.
    outerr = subprocess.Popen("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.find( { uploadedAt: { $lt: ISODate(\""""+start_date+"""\") } } ).forEach(printjson);'""", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = outerr.communicate()
    out = out.replace("\n","").replace("\t","")
    #This then RE the file ids out
    oldfileIDS = re.findall(r'\_id\"\s\:\s\"(\w+?)\"',out)
    #iterates over the id's and removes them from the database
    for id in oldfileIDS:
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.chunks.remove({ files_id : {$eq : \""""+id+ """\"}})'""", shell=True)
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.files.remove({ _id : {$eq : \""""+id+ """\"}})'""", shell=True)
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.remove({ _id : {$eq : \""""+id+ """\"}})'""", shell=True)


if __name__ == "__main__":
	main()
