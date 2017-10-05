# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_big_gql 1'] = {
    'data': {
        'viewer': {
            'profile': {
                'tradingAccounts': {
                    'edges': [
                        {
                            'node': {
                                'accountName': 'testAccount1',
                                'trades': {
                                    'edges': [
                                        {
                                            'node': {
                                                'quantity': 1,
                                                'stock': {
                                                    'name': 'Google',
                                                    'ticker': 'GOOGL',
                                                    'trades': {
                                                        'edges': [
                                                            {
                                                                'node': {
                                                                    'account': {
                                                                        'accountName': 'testAccount1'
                                                                    }
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            },
            'username': 'testuser1'
        }
    }
}

snapshots['test_mutation 1'] = {
    'data': {
        'addTradingAccount': {
            'account': {
                'accountName': 'Test 1'
            }
        }
    }
}

snapshots['test_mutation_add_trading_account 1'] = {
    'data': {
        'addTradingAccount': {
            'account': {
                'accountName': 'Test 1'
            }
        }
    }
}
