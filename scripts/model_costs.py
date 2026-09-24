"""Provider usage and dated public-rate estimates, never invoice amounts."""
VERIFIED_ON = '2026-09-20'
GLM_PRICING = 'https://docs.z.ai/guides/overview/pricing'
JEV_PRICING = 'https://docs.typesafe.ai/models'


def count(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def normalized(provider, raw):
    raw = raw if isinstance(raw, dict) else {}
    keys = ('prompt_tokens', 'completion_tokens') if provider == 'glm' else ('input_tokens', 'output_tokens')
    incoming, outgoing = (count(raw.get(k)) for k in keys)
    detail = raw.get('prompt_tokens_details') or {}
    cached = count(detail.get('cached_tokens')) if provider == 'glm' and isinstance(detail, dict) else None
    return {'input_tokens': incoming, 'output_tokens': outgoing, 'cached_input_tokens': cached,
            'total_tokens': incoming+outgoing if incoming is not None and outgoing is not None else None}


def estimate(provider, model, usage):
    if model == 'glm-5.3' and provider == 'glm':
        rates, source = {'input': 1.4, 'cached_input': .26, 'output': 4.4}, GLM_PRICING
    elif model == 'jev-1.13.0' and provider == 'jev':
        rates, source = {'input': .042, 'cached_input': .042, 'output': 0}, JEV_PRICING
    else:
        return {'usd': None, 'reason': 'No verified price for this model.', 'verified_on': VERIFIED_ON}
    result = {'usd': None, 'currency': 'USD', 'basis': 'Estimated token cost; not an invoice.',
              'pricing_url': source, 'verified_on': VERIFIED_ON, 'per_million_tokens': rates,
              'excludes': 'Unreported attempts, credits, taxes, discounts, storage and transfer.'}
    incoming, outgoing, cached = (usage.get(k) for k in ('input_tokens', 'output_tokens', 'cached_input_tokens'))
    if count(incoming) is None or count(outgoing) is None:
        result['reason'] = 'Provider token usage unavailable or inconsistent.'
        return result
    if cached is not None and (count(cached) is None or cached > incoming):
        result['reason'] = 'Invalid provider cached-token count.'
        return result
    if cached is None:
        cached = 0
        if provider == 'glm':
            result['assumption'] = 'Cache usage unreported; estimate assumes all input is uncached.'
    result['usd'] = ((incoming-cached)*rates['input'] + cached*rates['cached_input'] + outgoing*rates['output'])/1_000_000
    return result


def comparison(result):
    """Compare pipeline stages; never imply equal inputs or interchangeable outputs."""
    usage = result['usage']
    tokens = normalized('jev', usage)
    model = ', '.join(usage['models']) or result['model']
    cost = estimate('jev', model, tokens)
    if usage['unreported_attempts']:
        cost.update(known_usage_usd=cost['usd'], usd=None,
                    reason='Some attempts have no reported usage; total cost is unknown.')
    rows = [{'provider': 'jev', 'model': model, 'role': 'Research search, typed judgments and design checks',
             'status': 'success' if result['judgments'] else 'incomplete', 'tokens': tokens, 'cost': cost,
             'api_requests': usage['api_requests'], 'cached_requests': usage['cached_requests'],
             'unreported_attempts': usage['unreported_attempts']}]
    if result['mode'] == 'written':
        row = {'provider': 'glm', 'model': 'glm-5.3', 'role': 'Explanation from selected evidence',
               'status': 'not_run', 'tokens': normalized('glm', {}),
               'cost': {'usd': 0, 'reason': 'No writer request made.'}}
        row.update(result.get('writer', {}))
        rows.append(row)
    amounts = [r['cost']['usd'] for r in rows]
    return {'rows': rows, 'total_estimated_usd': sum(amounts) if all(v is not None for v in amounts) else None,
            'scope': 'Different stages of this query: Jev searches, assesses and checks; GLM writes from selected evidence. This is not an equal-workload benchmark.',
            'cost_note': 'Tokens cover new requests with reported usage in this run. Reused local Jev evaluations add no new request or tokens. Estimates use published rates verified on '+VERIFIED_ON+'; actual charges may differ. Unreported attempts make the total unknown.'}
