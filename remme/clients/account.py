# Copyright 2018 REMME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------

from remme.protos.account_pb2 import AccountMethod, GenesisPayload, TransferPayload
from remme.clients.basic import BasicClient
from remme.tp.account import AccountHandler
from remme.shared.exceptions import KeyNotFound

from remme.protos.account_pb2 import Account


class AccountClient(BasicClient):
    def __init__(self):
        super().__init__(AccountHandler)

    def _send_transaction(self, method, data_pb, extra_addresses_input_output):
        addresses_input_output = [self.get_user_address()]
        if extra_addresses_input_output:
            addresses_input_output += extra_addresses_input_output
        return super()._send_transaction(method, data_pb, addresses_input_output)

    @classmethod
    def get_transfer_payload(self, address_to, value):
        transfer = TransferPayload()
        transfer.address_to = address_to
        transfer.value = value

        return transfer

    @classmethod
    def get_genesis_payload(self, total_supply):
        genesis = GenesisPayload()
        genesis.total_supply = int(total_supply)

        return genesis

    @classmethod
    def get_account_model(self, balance):
        account = Account()
        account.balance = int(balance)

        return account

    def transfer(self, address_to, value):
        extra_addresses_input_output = [address_to]
        transfer = self.get_transfer_payload(address_to, value)

        return self._send_transaction(AccountMethod.TRANSFER, transfer, extra_addresses_input_output)

    def get_account(self, address):
        account = Account()
        account.ParseFromString(self.get_value(address))
        return account

    def get_pub_keys(self, address):
        try:
            account = self.get_account(address)
            return list(account.pub_keys)
        except KeyNotFound:
            return []

    def get_balance(self, address):
        try:
            account = self.get_account(address)
            return account.balance
        except KeyNotFound:
            return 0
