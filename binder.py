#!/usr/bin/env python2.7

import codecs
import os
import re
import sqlite3
from collections import defaultdict
import ldap
import getpass

from config import *

# woo regular expressions
NAME_RE = re.compile(r'<title>UNSW Handbook Course - (.*?) - [A-Z]{4}[0-9]{4}</title>', re.DOTALL)
DESC_RE = re.compile(r'<!-- Start Course Description -->(.*?)<!-- End Course description -->', re.DOTALL | re.IGNORECASE)

COURSE_RE = re.compile(r'[A-Z]{4}[0-9]{4}', re.IGNORECASE)
BR_RE = re.compile(r'<br ?/?>', re.IGNORECASE)
TAG_RE = re.compile(r'</?.*?>')

'''
# set up ldap connection
print 'pls enter ldap stuff'

user = raw_input('zID: ')
upn = user + '@ad.unsw.edu.au'

password = getpass.getpass()

print 'Opening connection...'
ldap_conn = ldap.open('localhost', port=1337)
ldap_conn.protocol_version = ldap.VERSION3
print 'Binding...'
ldap_conn.bind_s(upn, password)
print 'OK'
'''

if os.path.exists(DATABASE_FILENAME):
    print 'Deleting existing database'
    os.unlink(DATABASE_FILENAME)

print 'Creating new database'
conn = sqlite3.connect(DATABASE_FILENAME)
cur = conn.cursor()

print 'Creating tables'
cur.execute('''
CREATE TABLE courses (
    code text primary key,
    name text,
    description text
)
''')

cur.execute('''
CREATE TABLE offerings (
    id integer primary key autoincrement,
    code text,
    year integer,
    session text
)
''')

cur.execute('''
CREATE TABLE lecturings (
    offering_id integer,
    lecturer_id integer
)
''')

cur.execute('''
CREATE TABLE lecturers (
    id integer primary key autoincrement,
    surname text,
    given_names text
)
''')

# user stuff
cur.execute('''
CREATE TABLE users (
    zid text primary key,
    first_name text,
    surname
)
''')

cur.execute('''
CREATE TABLE ratings (
    offering_id integer,
    content_rating integer,
    lecturer_rating integer,
    difficulty_rating integer,
    comment text,
    user_id text
)
''')

'''
print 'Loading passwd'
print

full_names = []
is_expired = {}

f = open(PASSWD_FILENAME)
for line in f:
    fields = line.rstrip().split(':')

    if ',' not in fields[4]:
        continue

    name, title = fields[4].split(',', 1)
    username = fields[0]

    if title != 'Student' and re.match(r'^[a-z]+$', username):
        name = re.sub(r'([a-z])([A-Z])', '\1 \2', name)
        name = name.replace('El Gindy', 'Elgindy') # there you go, hossam elgindy

        full_names.append(name)
        if not fields[-1].endswith('EXPIRED'):
            if name in is_expired:
                is_expired[name] = False
        else:
            if name not in is_expired:
                is_expired[name] = True
f.close()
'''

print 'Loading timetable'

warnings = []

lecturer_names = set()

# keep track of shit in the db
lecturer_ids = {}
course_codes = set()

for year in xrange(CURRENT_YEAR, MIN_YEAR-1, -1):
    print year
    tt_directory = '%s/%d' % (TIMETABLE_DIR, year)
    hb_directory = '%s/%d' % (COURSES_DIR, year)
    filenames = os.listdir(tt_directory)
    for filename in filenames:
        course = filename.rstrip('.html')

        # read handbook entry
        f = codecs.open('%s/%s' % (hb_directory, filename), encoding='utf-8')
        data = f.read()
        f.close()

        # strip &nbsp;'s and <strong> tags
        data = data.replace('&nbsp;', ' ')
        data = data.replace('<strong>', '')
        data = data.replace('</strong>', '')

        # find name
        match = re.search(NAME_RE, data)
        if match:
            course_name = match.group(1).strip().replace('\n', '')
        else:
            course_name = None
            print "Couldn't find name"
            print 'Fatal error!'
            quit()

        # find description
        match = re.search(DESC_RE, data)
        if match:
            desc = match.group(1).strip()
        else:
            desc = None
            print "Couldn't find description"

        if course not in course_codes:
            # add to db
            cur.execute('''
            INSERT INTO courses (
                code, name, description
            ) VALUES (
                ?, ?, ?
            )
            ''', (course, course_name, desc))

            course_codes.add(course)

        print '  %s %s' % (course, course_name)

        # now, read timetable
        f = open('%s/%s' % (tt_directory, filename))
        data = f.read()
        f.close()

        session_staff = defaultdict(list)
        session_contacts = defaultdict(list)

        sessions = re.split(r'<a name="([A-Z][0-9])"></a>', data, re.M)
        for session in sessions:
            m = re.search(r'<td valign="top" class="classSearchSectionHeading"> *([^<]+) CLASSES - Detail *</td>', session)
            if m:
                #print '  %s' % m.group(1)

                m = re.search(r'<a name="([A-Z][0-9])-[0-9]+"></a>', session)
                if m:
                    session_code = m.group(1)

                    # world's best regex award goes to: me
                    classes = re.findall(r'^ {33}<table width="100%" cellspacing="0">(.*?)^ {33}</table>', session, re.S | re.M)
                    #print len(classes), 'classes found'
                    for class_ in classes:
                        m = re.search(r'<td class="data">[^<]*Lecture[^<]*</td>', class_)
                        if m:
                            # it's a lecture!
                            # now find staff names
                            m = re.search(r'^ {42}<table width="100%" cellspacing="0">(.*?)^ {42}</table>', class_, re.S | re.M)
                            if m:
                                details = m.group(1)

                                class_staff = re.findall(r'<td class="data">([^<]*)</td>\s*</tr>', details)
                                session_staff[session_code] += class_staff

            m = re.findall(r'<td class="data">([A-Z][0-9])</td>\n {45}</tr>\n {42}</table>\n {39}</td>\n {39}<td class="data">(.*?)</td>', session, re.M)
            for session_code, name in m:
                session_code = session_code.replace('U', 'X').replace('T', 'S')
                session_contacts[session_code].append(name)

        def normalise_staff(staff):
            # split on ,
            staff_, staff = staff, []
            for s in staff_:
                for name in s.split(','):
                    name = name.strip()
                    if name and name != 'School Office':
                        name = re.sub(r' +', ' ', name) # remove duplicate spaces
                        name = re.sub(r' van ', ' van ', name, flags=re.I) # there you go, ron van der meyden

                        name = name.split(' ', 1)[1] # remove title
                        staff.append(name)
            staff = list(set(staff)) # remove duplicates

            return staff

        for session_code in sorted(set(session_staff.keys()).union(set(session_contacts.keys()))):
            staff = normalise_staff(session_staff[session_code])
            contacts = normalise_staff(session_contacts[session_code])

            #print '  %s: lecturers %s, staff contact %s' % (session_code, staff, contacts)

            # if there are no staff found, use contacts instead
            if len(staff):
                lecturers = staff
            else:
                lecturers = contacts

            print '    %s: %s' % (session_code, ', '.join(lecturers))
            if not len(lecturers):
                warnings.append('WARNING: no lecturers in %s %d%s' % (course, year, session_code))

            # add to db
            res = cur.execute('''
            INSERT INTO offerings (
                code, year, session
            ) VALUES (
                ?, ?, ?
            )
            ''', (course, year, session_code))

            offering_id = cur.lastrowid

            for lecturer in lecturers:
                given_names, surname = lecturer.split(' ', 1)
                
                # check if already there
                lecturer_id = lecturer_ids.get((given_names, surname))
                if not lecturer_id:
                    cur.execute('''
                    INSERT INTO lecturers (
                        surname, given_names
                    ) VALUES (
                        ?, ?
                    )''', (surname, given_names))

                    lecturer_id = cur.lastrowid
                    lecturer_ids[(given_names, surname)] = lecturer_id

                cur.execute('''
                INSERT INTO lecturings (
                    offering_id, lecturer_id
                ) VALUES (
                    ?, ?
                )''', (offering_id, lecturer_id))

'''
all_staff = []

baseDN = 'OU=IDM_People,OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au'
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = ['givenName', 'middleName', 'sn', 'initials', 'memberOf']
searchFilter = '(|(memberOf=CN=ROLE_PTR_CSESTAFF_USERS,OU=ROLE,OU=Groups,OU=CSE,OU=ENG,OU=OneUNSW,DC=ad,DC=unsw,DC=edu,DC=au)(&(department=Computer Science & Engineering)(homeDirectory=*Staff*)(description=*Alumni*)))'

result = ldap_conn.search(baseDN, searchScope, searchFilter, retrieveAttributes)
_, data = ldap_conn.result(result, 1000)

print '%d results' % len(data)

for _, attr_results in data:
    try:
        surname = attr_results['sn'][0]
        given_names = attr_results['givenName'][0]
        if 'middleName' in attr_results:
            given_names += ' ' + attr_results['middleName'][0]

        all_staff.append((given_names, surname))
    except:
        print 'fuck', attr_results

for lecturer in lecturer_names:
    tt_initials, tt_surname = lecturer.split(' ', 1)

    candidates = []
    for given_names, surname in all_staff:
        if surname == tt_surname:
            candidates.append('%s %s' % (given_names, surname))

    print tt_initials, tt_surname, candidates

exit(0)
'''

"""

#print '\n'.join(warnings)
exit(0)

print 'Loading course list'
print

filenames = os.listdir(COURSE_DIR)

i = 0
for filename in filenames:
    i += 1
    code = filename.rstrip('.html')
    print 'Reading %s (%d/%d)' % (code, i, len(filenames))

    # open with unicode support
    f = codecs.open('%s/%s' % (COURSE_DIR, filename), encoding='utf-8', mode='r')
    data = f.read()
    f.close()

    # strip &nbsp;'s and <strong> tags
    data = data.replace('&nbsp;', ' ')
    data = data.replace('<strong>', '')
    data = data.replace('</strong>', '')

    # find name
    match = re.search(NAME_RE, data)
    if match:
        name = match.group(1).strip().replace('\n', '')
        print 'Found name:', name
    else:
        name = None
        print "Couldn't find name"
        print 'Fatal error!'
        quit()

    # find description
    match = re.search(DESC_RE, data)
    if match:
        desc = match.group(1).strip()
        print 'Found description'
    else:
        desc = None
        print "Couldn't find description"

    print 'Writing to database'
    cur.execute('''
    INSERT INTO courses (
        code, name, description, prerequisites, corequisites, exclusions, gened, outline, uoc
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (code, name, desc, prereqs, coreqs, exclusions, gened, outline, uoc))
    ''')

"""

conn.commit()
conn.close()
