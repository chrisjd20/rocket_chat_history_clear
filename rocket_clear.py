#!/usr/bin/env python
#use at own risk
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
    start_date = str(datetime.datetime.now() + datetime.timedelta(-30))[:10]
    subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_message.remove( { ts: { $lt: ISODate(\""""+start_date+"""\") } } );'""", shell=True)
    outerr = subprocess.Popen("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.find( { uploadedAt: { $lt: ISODate(\""""+start_date+"""\") } } ).forEach(printjson);'""", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = outerr.communicate()
    out = out.replace("\n","").replace("\t","")
    oldfileIDS = re.findall(r'\_id\"\s\:\s\"(\w+?)\"',out)
    for id in oldfileIDS:
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.chunks.remove({ files_id : {$eq : \""""+id+ """\"}})'""", shell=True)
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.files.remove({ _id : {$eq : \""""+id+ """\"}})'""", shell=True)
        subprocess.call("""/usr/bin/mongo localhost/parties --eval 'db.rocketchat_uploads.remove({ _id : {$eq : \""""+id+ """\"}})'""", shell=True)


if __name__ == "__main__":
	main()
