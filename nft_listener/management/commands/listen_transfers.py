from web3 import Web3
from django.core.management.base import BaseCommand
from nft_listener.models import TransferEvent
from django.conf import settings

INFURA_KEY = settings.INFURA_KEY
CONTRACT_ADDRESS = settings.CONTRACT_ADDRESS
START_BLOCK = int(settings.START_BLOCK)
END_BLOCK = int(settings.END_BLOCK)

class Command(BaseCommand):
    help = 'Listens for BAYC Transfer events and save events data in the sqlite database'

    def handle(self, *args, **kwargs):
        """
        Connects to Ethereum mainnet via infura and listens for BAYC Transfer events.
        Each event is saved in the sqlite database.
        """
        infura_url = f"https://mainnet.infura.io/v3/{INFURA_KEY}"
        web3 = Web3(Web3.HTTPProvider(infura_url))

        # Check connection to Ethereum mainnet
        if not web3.is_connected():
            print(self.style.ERROR("Could not connect to Ethereum mainnet"))
            return

        # Create BAYC contract object with address and minimal ABI
        bayc_contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
        bayc_abi = [{
            "anonymous": False,
            "inputs": [
                { "indexed": True, "name": "from", "type": "address" },
                { "indexed": True, "name": "to", "type": "address" },
                { "indexed": True, "name": "tokenId", "type": "uint256" }
            ],
            "name": "Transfer",
            "type": "event"
        }]
        contract = web3.eth.contract(address=bayc_contract_address, abi=bayc_abi)

        # Create a filter for the Transfer events within the specified block range
        try:
            transfer_filter = contract.events.Transfer.create_filter(
                fromBlock=START_BLOCK,
                toBlock=END_BLOCK
            )
        except ValueError as e:
            print(self.style.ERROR(f"Failed to create filter: {e}"))
            return

        print(self.style.SUCCESS("Listening for BAYC Transfer events..."))

        # Fetch Transfer events within the specified block range
        for event in transfer_filter.get_all_entries():
            token_id = event['args']['tokenId']
            from_address = event['args']['from']
            to_address = event['args']['to']
            transaction_hash = event['transactionHash'].hex()
            block_number = event['blockNumber']

            # Save to the database
            TransferEvent.objects.create(
                token_id=token_id,
                from_address=from_address,
                to_address=to_address,
                transaction_hash=transaction_hash,
                block_number=block_number
            )
            print(self.style.SUCCESS(
                f"Transfer Event: Token ID {token_id}, From {from_address}, To {to_address}"
            ))