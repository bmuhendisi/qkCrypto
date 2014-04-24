__author__ = 'Jakehp'
import qkCommChannel


class qkComm(object):

    PHOTON_PULSE_SIZE = 128
    MIN_SHARED_REQ = 25

    def __init__(self):
        self.random_basis = []
        self.other_basis = []
        self.photon_polars = []
        self.shared_key = []
        self.sub_shared_key = []
        self.decision = -1
        self.other_decision = -1
        self.valid_key = -1

#BASIS STUFF
    #Retrieve sender basis's and check against local random basis
    def check_other_basis(self, insecure_comm_channel):
        assert isinstance(insecure_comm_channel, qkCommChannel.qkCommChannel), 'Invalid Arg'
        #Retrieve & Remove sender basis from communication channel
        if self.PHOTON_PULSE_SIZE == len(insecure_comm_channel.basis_check):
            self.other_basis = insecure_comm_channel.basis_check.copy()
            insecure_comm_channel.basis_check.clear()

    #Compare sent and received basis
    def compareBasis(self):
        if len(self.other_basis) == self.PHOTON_PULSE_SIZE and len(self.random_basis) == self.PHOTON_PULSE_SIZE and len(self.recorded_polarizations) == self.PHOTON_PULSE_SIZE:
            i = 0
            count = 0
            while i < self.PHOTON_PULSE_SIZE:
                if self.random_basis[i] == self.other_basis[i]:
                    count += 1
                i += 1

    #Send basis to a qkCommChannel for a sender/Alice
    def send_basis(self, insecure_channel, basisC):
        assert isinstance(insecure_channel, qkCommChannel.qkCommChannel), 'Invalid Arg1'
        insecure_channel.basis_check = basisC

#POLAR STUFF
        #Drops any polarizations where the sender and receiver basis differ'd
    def drop_invalid_polars(self):
        if len(self.other_basis) == self.PHOTON_PULSE_SIZE and len(self.random_basis) == self.PHOTON_PULSE_SIZE and len(self.photon_pulse) == self.PHOTON_PULSE_SIZE and len(self.photon_polars) == self.PHOTON_PULSE_SIZE:
            i = 0
            max = self.PHOTON_PULSE_SIZE
            while i < max:
                if self.random_basis[i] != self.other_basis[i]:
                    self.random_basis.pop(i)
                    self.other_basis.pop(i)
                    self.photon_polars.pop(i)
                    self.photon_pulse.pop(i)
                    max -= 1
                else:
                    i += 1
        else:
            print("Error - Required Data Not Initialized.")

#BIT AND SUBBIT STRING STUFF
    #what happened here...
    #Analyzes the recorded polarizations to determine the shared key received from a sender through a channel.
    def set_bit_string(self):
        self.shared_key.clear()
        if len(self.photon_polars) <= self.PHOTON_PULSE_SIZE and len(self.photon_polars) > 0:
            i = 0
            while i < len(self.photon_polars):
                if self.photon_polars[i] == 0:
                    self.shared_key.append(0)
                elif self.photon_polars[i] == 90:
                    self.shared_key.append(1)
                elif self.photon_polars[i] == 45:
                    self.shared_key.append(0)
                elif self.photon_polars[i] == 135:
                    self.shared_key.append(1)
                i += 1

    #Retrieve a subBitString from a qkCommChannel
    def get_sub_bit_string(self, insecure_channel):
        self.sub_shared_key.clear()
        assert isinstance(insecure_channel, qkCommChannel.qkCommChannel), 'Invalid Arg1'
        if len(insecure_channel.sub_shared_key) > 0:
            self.sub_shared_key = insecure_channel.sub_shared_key.copy()
            insecure_channel.sub_shared_key.clear()
        else:
            print("Error - qkCommChannel has no bit sub string.")

    #Sends a subBitString to a qkCommChannel, the sub key is just shared_key[0->approx half]
    def send_sub_bit_string(self, insecure_comm_channel):
        assert isinstance(insecure_comm_channel, qkCommChannel.qkCommChannel), 'Invalid Arg1'
        insecure_comm_channel.sub_shared_key.clear()
        if len(self.shared_key) > 0:
            insecure_comm_channel.sub_shared_key = (self.shared_key[0: (int((len(self.shared_key))/2))]).copy()

#DECISION STUFF
    #Sends a decision to a qkCommChannel
    def send_decision(self, insecure_comm_channel):
        assert isinstance(insecure_comm_channel, qkCommChannel.qkCommChannel), 'Invalid Arg1'
        if self.decision != -1:
            insecure_comm_channel.decision = self.decision
        else:
            print("Error - send_decision() - decision - Invalid")

    #Retrieves a decision value from a qkCommChannel
    def get_decision(self, insecure_comm_channel):
        assert isinstance(insecure_comm_channel, qkCommChannel.qkCommChannel), 'Invalid Arg1'
        if insecure_comm_channel != -1:
            self.other_decision = insecure_comm_channel.decision
            if self.decision == 1 and self.other_decision == 1:
                self.valid_key = 1
            else:
                self.valid_key = 0
        else:
            print("Error - send_decision() - decision - Invalid")

    #Decides if a sub shared key is valid enough, to validate a shared key
    def decide(self):
        if len(self.sub_shared_key) > 0 and len(self.shared_key) > len(self.sub_shared_key):
            i = 0
            count = 0
            while i < len(self.sub_shared_key):
                if self.sub_shared_key[i] == self.shared_key[i]:
                    count += 1
                i += 1
            if count >= self.MIN_REQ_OF_SHARED:
                self.decision = 1
            else:
                self.decision = 0
        else:
            self.decision = 0
            print("Error - decide() - othersub_shared_key || shared_key - Invalid")