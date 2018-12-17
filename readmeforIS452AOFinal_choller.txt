This code was created for Carissa Phillips’ final project in IS452AO Foundations of Information Processing, Fall 2018, taken through the iSchool at the University of Illinois at Urbana-Champaign.  The purpose of the code is to convert text from the “Directory of Directors in the City of Chicago” 1900/1901 into a data file of the form:

[person lastname], [person firstname], [organization]



Inputs:


The “Directory of Directors in the City of Chicago” (Chicago DoD) is a six-volume set produced between 1900/1901 and 1906, which has been digitized and made available through the Hathi Trust Digital Library (https://catalog.hathitrust.org/Record/100150493).  
 
Text-only output was generated through the Hathi Trust Digital Library for the 1900/1901 volume of the Chicago DoD. The directory portion (less the advertisements at the beginning and the appendices) was copied into one large text file in Notepad and named “DoDChicago1900-1901raw.txt.”  



Code:


The code began by opening “DoDChicago1900-1901raw.txt” using read() and creating an outfile, “DoDChicago1900_names.txt.”


infile = open('DoDChicago1900-1901raw.txt', 'r')
text = infile.read()
infile.close()
outfile = open('DoDChicago1900_names.txt', 'w')


The original infile had very few line breaks within each “page,” so the first task was to use “replace” to insert breaks where they appeared in the text image, i.e., after "Director." or "Manager."  This relies on there being a period (.) after the text to indicate the end of a line (in the original image), and in some cases, the assumption of having a period at the end of each line was shown to not be true.


dir_break = text.replace("ector.", "ector.\n")
dir_and_trustee_break = dir_break.replace("Trustee.", "Trustee.\n")


In the next section of code, headers were removed from the pages to clean up the text a bit.  Six recurring headers that were not needed were replaced with spaces in the output.


headerfree1 = dir_and_trustee_break.replace("DIRECTORY OF DIRECTORS.", "")
headerfree2 = headerfree1.replace("DIRECTORY OP DIRECTORS.", "")
headerfree3 = headerfree2.replace("THE AUDIT COMPANY OF NEW YORK.", "")
headerfree4 = headerfree3.replace("THE AUDIT COMPANY OP NEW YORK.", "")
headerfree5 = headerfree4.replace("DIRECTORY OF DIRECTORS IN THE CITY OF CHICAGO.", "")
headerfree6 = headerfree5.replace("DIRECTORY OF DIRECTORS OF CHICAGO.", "")


All of this organizing and “decluttering” of the text file resulted in a file called “textlist.”


textlist = headerfree6.split('\n')


Python then looped over each of the lines in sequence:


for line in textlist[0:]:

Visual inspection of the page image shows that on lines with personal names, the position of the first comma is an indication of the end of the last name, so the first instance of a comma in the line was located. The code then looked for the position of the second comma, which in lines with personal names indicates the end of the first name and middle initial (if present). 


firstcomma = (line.find(","))
secondcomma = firstcomma + (line[firstcomma+1:].find(",")) + 2


Next, the letters up to the first comma were named “firstword” and the letters between the first comma and second comma “secondword.”  These may be pieces of personal names, or pieces of an organization name; that determination comes later in the code.


firstword = line[0:firstcomma]
secondword = line[firstcomma:secondcomma]


Through visual inspection again, the consistent (within the limits of the OCR) presence of a period after the personal address was used to find the location of that period, and then extract the text between the second comma into a variable called “address.”


period_after_address = secondcomma + (line[secondcomma:].find("."))+2
address = line[secondcomma+1:period_after_address]


Finally, “find” was used again to locate the position of the word “Director.” which (visually) appears at the end of almost every line. Nine spaces were added to get to the end location of the line.  A variable, “orgrole,” was defined and the text between the “period_after_address” and the ending position of “Director.” plus 9 spaces was extracted into this variable.


dir_after_org1 = period_after_address + (line[period_after_address:].find("Director."))+9
orgrole = line[period_after_address:dir_after_org1] 


“If” statements were then incorporated to examine the cases of the words/phrases at the start of each line.  As visual examination has shown, the personal names are the only words that ever appear in uppercase letters.  So, the first test in the “if” statement was to see whether either of the words that start a line are in all uppercase.  If either the firstword OR secondword are found to be uppercase, they were renamed to be lastname and firstname, respectively, and then printed out along with the organization and roles.


if firstword.isupper() or secondword.isupper():
	lastname = firstword
	firstname = secondword
	print(lastname.strip()+firstname.strip(), orgrole.strip())
	print(lastname.strip()+firstname.strip(), orgrole.strip(), file=outfile)


Next, within an “elif” statement, Python to evaluated the lines in which the first word was not uppercase.  A condition was added to the elif line to make sure that there was a comma, since that confusion (when there wasn’t a comma) was causing lines to be missed and not printed.  Then, Python considered whether the firstword in those lines was in “title” case (.istitle). With those conditions both met, an organization line was identified, and the last values of lastname and firstname were printed along with that current line which was going through the loop.


elif firstcomma > -1 and firstword.istitle():
	print(lastname.strip()+firstname.strip(), line.strip())
	print(lastname.strip()+firstname.strip(), line.strip(), file=outfile)



Outputs:


Within the limits of consistent punctuation and spelling and accurate OCR, the output file looks like this snippet:

AARON, JACOB, Aaron Electric Co., President, Treasurer, Manager and Director.
ABBOTT, C. A., ? Abbott Alkaloidal Co., The, Director.
ABBOTT, EDWIN F., Charles W. Shonk Co., Director.
ABBOTT, W. L., Stockham Manufacturing Co., Director.
ABBOTT, WALLACE C, Abbott Alkaloidal Co., The, President, Manager and Director.
ABBOTT, WALLACE C, Clinic Publishing Co., The, President and Director ABEL, HOWARD, 169 Jackson Boulevard. Chicago & Harlem Street Railway Co., Secretary, Treasurer and Director.
ABBOTT, WALLACE C, Lake Street Elevated R.R. Co., President and Director.
ABBOTT, WALLACE C, Northwestern Elevated R.R. Co., Treasurer and Director.
ABBOTT, WALLACE C, Union Elevated R.R. Co., Treasurer and Director.
ABELE, AUGUST, Western Shade Cloth Co., The, Vice-President, Treasurer and Director.
ABEN, CHARLES, Western Planing & Manufacturing Co., Secretary, Treasurer, Manager and Director.
ABRAHAM, CHARLES, Illinois Moulding Co., The, Vice-President and Director.
ABRAHAMSON, JOHN, Chicago Tailoring Co., Director.
ABRAMS, W. H., Abstract Safety Vault Co., Secretary and Director.
ACKERS, THOMAS B., Illinois Life Insurance Co., Director.
ACKERT, C. H., Chicago, Lake Shore & Eastern Railway Co., Director.
ACKERT, C. H., Elgin, Joliet & Eastern Railway Co., President and Director.
ADAM, ALEXANDER B., Edson Keith & Co., Vice-President and Director.
ADAMS, B. F., American Tube Co., Vice-President and Director.
ADAMS, C. W., Federal Life Insurance Co., Director.
ADAMS, C. W., Federal Underwriting Co., Director.
ADAMS, F. W., American Tube Co., President and Director.
ADAMS, GEORGE, George Adams & Burke Co., President, Treasurer, Manager and Director.
ADAMS, GEORGE E., Calumet Electric Street Railway Co., The, Director.
ADAMS, GEORGE E., South Side Elevated R.R. Co., Director.


Some corrections need to be made yet, either manually in the text or in the code, but overall this code successfully creates lines with personal last names, first names, and organizational affiliations, and repeats last and first names where multiple organization affiliations for a single person are presented. 
