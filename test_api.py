from signalwire.rest import Client as signalwire_client

client = signalwire_client("981ab3f3-3bee-408f-ad96-5ebe87c318ac", "PT44f71ed3fd40a1fc83e1d8d67a4b80f200b0862c5675d794", signalwire_space_url = 'shashi-fs.signalwire.com')

members = client.queues('a2bff28a-8dce-4dca-b36f-1bcca187a563').members.list()
members_count = len(members)
print(members)
print(members_count)
#for record in members:
#    print(record.call_sid)
