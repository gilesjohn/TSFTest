export { test, Test}

declare global {
    interface Window { runTests: Function; }
}

class Description {
    text: string
    success?: boolean

    constructor(text: string, success?: boolean) {
        this.text = text
        this.success = success
    }
}

class Assertion {
    success: boolean
    message: string

    constructor(success: boolean, message: string) {
        this.message = message
        this.success = success
    }
}

class Test {
    name: string;
    func: (test: Test) => void | Promise<void>;

    results: (Description | Assertion)[] = []

    constructor(name: string, func: (test: Test) => void | Promise<void>) {
        this.name = name
        this.func = func
    }

    passed() {
        return this.results.every((result) => result instanceof Description || result.success )
    }

    totalAssertions() {
        return this.results.filter((result) => result instanceof Assertion )
    }

    totalFailedAssertions() {
        return this.results.filter((result) => result instanceof Assertion && !result.success )
    }

    async run() {
        try {
            await this.func(this)
        } catch (e: any) {
            let error: Error
            if (e instanceof Error) {
                error = e
            } else {
                error = new Error(e.toString())
            }
            if (e instanceof AssertionError) {
                this.describe(`Test failed due to failed assertion`, false)
            } else {
                this.describe(`Test failed due to uncaught error\n${error.stack}`, false)
            }
        }
    }

    describe(description: string, success?: boolean) {
        this.results.push(new Description(description, success))
    }

    assert(result: any, expected: any) {
        let success = result === expected
        this.results.push(new Assertion(
            success,
            `Assertion ${success ? 'passed' : 'failed'}\nResult: ${result.toString()}\nExpected: ${expected.toString()}`
        ))
        if (!success) {
            throw new AssertionError()
        }
    }

    assertInstance(anInstance: any, aClass: Function) {
        let success = anInstance instanceof aClass
        this.results.push(new Assertion(
            success,
            `Assertion ${success ? 'passed' : 'failed'}\n${anInstance.toString()} is ${success ? '' : ' not'} an instance of ${aClass.name}`
        ))
        if (!success) {
            throw new AssertionError()
        }
    }
}

window.runTests = runTests;

let tests: Test[] = []
let isHeadless = false

function test(name: string, func: (test: Test) => void | Promise<void>) {
    tests.push(new Test(name, func))
}

class AssertionError extends Error {
    constructor(message?: string) {
        super(message)
    }
}

async function runTests(headless: boolean) {
    isHeadless = headless
    await Promise.all(tests.map((test) => test.run()))
    return tests
}