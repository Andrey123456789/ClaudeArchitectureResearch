"""C06B sample read: for each candidate, the first 5 hinted records by sha256('C06B|'+key), leaving out the R22 sample. Verdicts were written after reading the claim, the original field, the hint and the current source line. The verdict is on the hint: does it state a true scope for this record?"""


def row(key, verdict, why):
    return dict(key=key, verdict=verdict, why=why)


SAMPLE = [
    row('FG-M-ea83ed5043', 'RIGHT', 'Keeping persistence configuration out of Domain entities is a backend persistence matter.'),
    row('FG-M-8331b0e4cf', 'RIGHT', 'The build-fix step applies to a failing build or tests.'),
    row('FG-M-de1eacd1e3', 'RIGHT', 'The output format binds the delegated reviewer.'),
    row('FG-M-ea186381d4', 'RIGHT', 'Mocking guidance is about backend tests.'),
    row('FG-M-af23726db8', 'RIGHT', 'Stacked handlers and retry combinations are outbound resilience.'),
    row('FG-M1-77e103cfd2', 'RIGHT', 'Entity configuration is backend persistence.'),
    row('FG-M1-edfb80480c', 'RIGHT', 'Bounded iteration governs repair of a failing build or tests.'),
    row('FG-M1-4e3cc9936f', 'RIGHT', 'True of this line in add-dependency. The approved-technology duty also applies elsewhere, through other records.'),
    row('FG-M1-23639ed4d2', 'RIGHT', 'Log message templates are backend code. Coarse, but true.'),
    row('FG-M1-fe0a888f88', 'RIGHT', 'The line sits in the container guidance for local infrastructure.'),
    row('FG-L0-8e5a79ef88', 'RIGHT', 'Swagger configuration is API documentation.'),
    row('FG-L0-ddcb9deb02', 'RIGHT', 'Provider choice is backend persistence.'),
    row('FG-L0-76ba34035b', 'RIGHT', 'The status code mapping applies to backend Controllers.'),
    row('FG-L0-04b8f0eddf', 'DEBATABLE', 'The hint lists every manifest the hook reads. This claim is only about package.json, so it is wider than the record.'),
    row('FG-L0-e6cdfa2340', 'RIGHT', 'A review item of the security scan layer.'),
    row('FG-L1-64120344e7', 'RIGHT', 'True as the outer scope of the workflow. The claim states its narrower condition itself.'),
    row('FG-L1-844366a741', 'RIGHT', 'A reporting restraint for a security review.'),
    row('FG-L1-9bb25954cb', 'DEBATABLE', 'The workflow scope includes removal, and a deprecation check on the chosen version does not apply to removing a package.'),
    row('FG-L1-43f8511619', 'RIGHT', 'The diff review belongs to the check before finishing or preparing a PR.'),
    row('FG-L1-e112a31582', 'DEBATABLE', 'True, but it names only code areas. The real condition, permissions that depend on the resource, is in the claim and the status does not extract it.'),
    row('FG-K0-0e7e20f7a9', 'RIGHT', 'A reference change is inside that workflow scope. The claim states the narrower condition.'),
    row('FG-K0-f27a96c1a0', 'DEBATABLE', 'The workflow scope is any Git operation, and the claim applies only before pushing. The claim says so; the hint is wider.'),
    row('FG-K0-9178102800', 'DEBATABLE', 'As FG-L1-9bb25954cb: version selection does not apply to removal.'),
    row('FG-K0-3b9974dfd6', 'RIGHT', 'Result<T> guidance is backend. Coarse, but true.'),
    row('FG-K0-e1ebc473cf', 'RIGHT', 'Choosing checks belongs to the step before declaring implementation complete.'),
    row('FG-K1-976373dda1', 'RIGHT', 'Pagination ordering in the EF Core guidance is backend.'),
    row('FG-K1-64e9c9e171', 'RIGHT', 'Cache invalidation contracts are backend. The claim states the narrower condition.'),
    row('FG-K1-c0918232ca', 'RIGHT', 'Query collation is backend.'),
    row('FG-K1-3f4d6c85d3', 'RIGHT', 'Severity rating binds the security audit.'),
    row('FG-K1-e9f6f61c68', 'RIGHT', 'Applying the Reserved test is what that workflow scope covers.'),
]
