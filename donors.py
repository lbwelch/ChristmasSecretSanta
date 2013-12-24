import random

class Donor(object):
    """A class representing one Xmas recipient/donor."""
    def __init__(self, name, spouse = "nil", lastRecipient = "nil", recipient = "nil"):
        self.name = name
        self.spouse = spouse
        self.lastRecipient = lastRecipient
        self.recipient = recipient
    def str(self):
        return "%s - Recipient:%s LastRecipient:%s\n" % (self.name, \
                self.recipient, self.lastRecipient)

class Donors(object):
    """A class containing an entire family of Xmas donors."""
    def __init__(self, donorNames, spouses):
        """Donors.__init__() sets the name, spouse, and recipient for every 
        Donor in the family. Note that the last of these will only be valid
        for the first run. If there are recipients from previous years then
        shuffleRecipients() will need to be run again after setLastRecipients()
        has been called"""
        random.seed()             # Seed random generator for shuffles
        self.donors = {}
        for donorName in donorNames:
            self.donors[donorName] = Donor(donorName)
        for spouse in spouses.keys():
            self.donors[spouse].spouse = spouses[spouse]
        self.shuffleRecipients()

    def __shuffleTest(self):
        """shuffleTest() checks whether a shuffle has produced an illegal
        result, i.e. if a donor's recipient matches the donor's name, spouse,
        or lastRecipient. It allows a 5% chance per each recipient of getting 
        the same recipient twice in a row."""
        for donor in self.donors.values():
            # A fudgeFactor of 1 represents the 5% chance of getting the 
            # same recipient again.
            fudgeFactor = random.randint(1, 20)   
            if (donor.name == donor.recipient or 
                donor.spouse == donor.recipient or
                (donor.lastRecipient == donor.recipient and fudgeFactor != 1)):
                return False
        return True

    def __performShuffle(self):
        """performShuffle() employs random.shuffle() to shuffle the recipients
        for each Donor in the Donors list. It's purely an internal member and
        is called only by shuffleRecipients(). It doesn't check whether the 
        result is valid; that's done by shuffleTest()."""
        recipients = self.donors.keys()
        random.shuffle(recipients)
        for (donor, recipient) in zip(self.donors.keys(), recipients):
            self.donors[donor].recipient = recipient

    def shuffleRecipients(self):
        """shuffleRecipients() calls performShuffle() and shuffleTest()
        repeatedly until shuffleTest() reports that the result is valid."""
        self.__performShuffle()
        while (not self.__shuffleTest()):
            self.__performShuffle()

    def setRecipients(self, donorRecipients):
        """setRecipients receives a list of donor/recipient pairs separated by
        commas. If the number of recipients supplied matches the number of
        donors then the previous recipients are set for the donors in the order
        given."""
        if len(donorRecipients) != len(self.donors):
            raise IndexError, "setRecipients(): incorrect number of " \
                "recipients supplied."
        for donorRecipient in donorRecipients:
            (donor, recipient) = donorRecipient.split(':')
            self.donors[donor].recipient = recipient

    def setLastRecipients(self, lastRecipients):
        """setLastRecipients receives a list of recipients.  If the number of
        recipients supplied matches the number of donors then the previous
        recipients are set for the donors in the order given."""
        if len(lastRecipients) != len(self.donors):
            raise IndexError, "setLastRecipients(): incorrect number of " \
                "previous recipients supplied."
        for donor in lastRecipients.keys():
            self.donors[donor].lastRecipient = lastRecipients[donor]
            print "donor: %s, lastRecipient: %s" % (donor, lastRecipients[donor])
            
    def getDonor(self, donorName):
        for donor in self.donors:
            if (donor.name == donorName):
                return donor

    def str(self):
        donorsString = ""
        for donor in self.donors.values():
            donorsString += donor.str()
        return donorsString
