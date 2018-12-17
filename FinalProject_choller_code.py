#opening the text file and creating an outpur file
infile = open('DoDChicago1900-1901raw.txt', 'r')
text = infile.read()
infile.close()
outfile = open('DoDChicago1900_names.txt', 'w')


#Using "replace" on the text file to impose line breaks to match with the page images in Hathi Trust
#First running replace on "ector." and creating a new file called dir_break.
#Then running replace on dir_break to impose breaks at instances of Trustee.
dir_break = text.replace("ector.", "ector.\n")
dir_and_trustee_break = dir_break.replace("Trustee.", "Trustee.\n")


#Running the text with the line breaks (now called "dir_and_trustee_break" through a series of
#steps in which I replace variations of header text (which is clutter) with spaces.  Each
#line uses the file from the previous line as its input, so this is iterative.
headerfree1 = dir_and_trustee_break.replace("DIRECTORY OF DIRECTORS.", "")
headerfree2 = headerfree1.replace("DIRECTORY OP DIRECTORS.", "")
headerfree3 = headerfree2.replace("THE AUDIT COMPANY OF NEW YORK.", "")
headerfree4 = headerfree3.replace("THE AUDIT COMPANY OP NEW YORK.", "")
headerfree5 = headerfree4.replace("DIRECTORY OF DIRECTORS IN THE CITY OF CHICAGO.", "")
headerfree6 = headerfree5.replace("DIRECTORY OF DIRECTORS OF CHICAGO.", "")

#This is the list I created after all of the efforts above, with line breaks imposed at selected intervals
#and certain common headers replaced with blanks spaces.
textlist = headerfree6.split('\n')

#Running through each line in textlist in sequence:
for line in textlist[0:]:
    firstcomma = (line.find(","))                                           #finding the first instance of a comma. On lines with personal names, this gives the end of the last name.  On lines with organization names, this is part or all of the organization name.
    secondcomma = firstcomma + (line[firstcomma+1:].find(",")) + 2          #finding the position of the second comma, allowing for differences in spacing (+2, found by by trial-and-error).  On lines with personal names, this is the end of the first name and middle initial (if present).  On lines with organization names, this is part or all of the organization name.
    firstword = line[0:firstcomma]                                          #Extracting the letters up to the first comma
    secondword = line[firstcomma:secondcomma]                               #Extracing the letters between the first and second commas
    period_after_address = secondcomma + (line[secondcomma:].find("."))+2   #Finding the location of the period at the end of the person's address, allowing for spacing difference (+2, found by by trial-and-error).
    address = line[secondcomma+1:period_after_address]                      #Extracing the address, which visual examination shows appears between the second comma and first period.
    dir_after_org1 = period_after_address + (line[period_after_address:].find("Director."))+9       #Finding the location of "Director." at the end of a line, and then adding +9 to account for the length of that word.
    orgrole = line[period_after_address:dir_after_org1]                     #Extracting the first organization name and roles, which visual inspection shows occurs after the period at the end of the address and extends to the end of Director.
    if firstword.isupper() or secondword.isupper():                         #Checking the cases of the first word or second word.  Since visual inspection shows that only personal names are in uppercase, if either is uppercase then....
        lastname = firstword                                                        #I'm calling the first word "lastname"
        firstname = secondword                                                      #I'm calling the second word "firstname"
        print(lastname.strip()+firstname.strip(), orgrole.strip())                  #I'm printing out lastname, firstname, and the orgrole
        print(lastname.strip()+firstname.strip(), orgrole.strip(), file=outfile)
    elif firstcomma > -1 and firstword.istitle():                           #The first condition only works for the lines that have an uppercase word, for the lines that do not have an uppercase word:
        print(lastname.strip()+firstname.strip(), line.strip())                     #I'm asking Python to recall the last values stored in lastname and firstname (from the line that ran through the loop) and concatenate that lastname and firstname to this line, which contains only an organization
        print(lastname.strip()+firstname.strip(), line.strip(), file=outfile)
