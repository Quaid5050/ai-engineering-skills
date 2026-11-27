"""Deterministic trust-boundary fixture, not a model or production agent runtime."""
import hashlib
import json


def retrieve(documents, tenant, principal, can_read):
    # Filter before context construction. The authorization callback is trusted code.
    return [d for d in documents if d['tenant']==tenant and can_read(principal,d['id'])]


def action_digest(action):
    return hashlib.sha256(json.dumps(action,sort_keys=True,separators=(',',':')).encode()).hexdigest()


class Gateway:
    def __init__(self): self.approvals={};self.used=set();self.effects=[]
    def approve(self, trusted_actor, action, token):
        # This entrypoint belongs to the host/UI, never to the model's tools.
        self.approvals[token]=(trusted_actor,action_digest(action))
    def execute(self, principal, action, token, allowed, budget):
        if not isinstance(action,dict) or set(action)!={'tool','tenant','resource'}:raise ValueError('invalid schema')
        if action['tool']!='publish' or not all(isinstance(v,str) for v in action.values()):raise ValueError('unsupported tool')
        if budget<=0:raise PermissionError('budget exhausted')
        if not allowed(principal,action['tenant'],action['resource']):raise PermissionError('current access denied')
        if token in self.used:raise PermissionError('approval consumed; reconcile prior outcome')
        if self.approvals.get(token)!=(principal,action_digest(action)):raise PermissionError('approval mismatch')
        self.used.add(token);self.effects.append(dict(action));return 'synthetic receipt'
