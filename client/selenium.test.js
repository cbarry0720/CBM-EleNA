const webdriver = require("selenium-webdriver");

describe("webdriver", () => {
	test("markers exist", async () => {
		try {
			const driver = new webdriver.Builder().forBrowser("chrome").build();
			await driver.get("http://localhost:3000");
			await driver.wait(
				webdriver.until.elementLocated(
					webdriver.By.className("leaflet-container")
				),
				10000
			);

			await driver
				.findElement(webdriver.By.className("from"))
				.sendKeys("UMass Amherst");
			await driver
				.findElement(webdriver.By.className("to"))
				.sendKeys("Amherst College");
			await driver.findElement(webdriver.By.className("go")).click();
			const markers = await driver.wait(
				webdriver.until.elementsLocated(
					webdriver.By.className("leaflet-marker-icon")
				),
				10000
			);
			expect(markers.length).toBe(2);
			await driver.quit();
		} catch (error) {
			console.log(error);
		}
	}, 35000);

	test("route-exists", async () => {
		try {
			const driver = new webdriver.Builder().forBrowser("chrome").build();
			await driver.get("http://localhost:3000");
			await driver.wait(
				webdriver.until.elementLocated(
					webdriver.By.className("leaflet-container")
				),
				10000
			);

			await driver
				.findElement(webdriver.By.className("from"))
				.sendKeys("UMass Amherst");
			await driver
				.findElement(webdriver.By.className("to"))
				.sendKeys("Amherst College");
			await driver.findElement(webdriver.By.className("go")).click();
			const route = await driver.wait(
				webdriver.until.elementLocated(
					webdriver.By.className("leaflet-interactive")
				),
				10000
			);
			expect(route).toBeTruthy();
			await driver.quit();
		} catch (error) {
			console.log(error);
		}
	}, 35000);

	test("empty inputs", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("empty to input", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("from"))
			.sendKeys("UMass Amherst");

		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("empty from input", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("to"))
			.sendKeys("Amherst College");

		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("invalid inputs", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("from"))
			.sendKeys("gpwonagewpa");
		await driver
			.findElement(webdriver.By.className("to"))
			.sendKeys("gwopagpwahvhfds");
		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("invalid to input", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("from"))
			.sendKeys("UMass Amherst");
		await driver
			.findElement(webdriver.By.className("to"))
			.sendKeys("gpwonagewpa");
		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("invalid from input", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("from"))
			.sendKeys("gpwonagewpa");
		await driver
			.findElement(webdriver.By.className("to"))
			.sendKeys("Amherst College");
		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);

	test("same inputs", async () => {
		const driver = new webdriver.Builder().forBrowser("chrome").build();
		await driver.get("http://localhost:3000");
		await driver.wait(
			webdriver.until.elementLocated(
				webdriver.By.className("leaflet-container")
			),
			10000
		);

		await driver
			.findElement(webdriver.By.className("from"))
			.sendKeys("UMass Amherst");
		await driver
			.findElement(webdriver.By.className("to"))
			.sendKeys("UMass Amherst");
		await driver.findElement(webdriver.By.className("go")).click();
		const alert = await driver.wait(
			webdriver.until.alertIsPresent(),
			10000
		);
		await alert.accept();

		await driver.quit();
	}, 35000);
});
